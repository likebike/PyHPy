/**
 * jQuery AJAXify
 * 
 * AJAX-'ifies' any <form> or <a> using the specified method of the form.
 * 
 * Also sends the value of the button clicked, and the x/y if using <input type="image"/>
 * 
 * Updates and fixes contributed by Andrea Battaglia - Thanks!
 * Replaced Ajaxify.serializeForm() with $('form').serialize() as per comments from David Lee
 * 
 * @package jquery-ajaxify
 * @author Dom Hastings
 * @author Andrea Battaglia
 */
(function($) {
  /**
   * jQuery.ajaxify
   * 
   * The main wrapper method for the Ajaxify object.
   * 
   * This adds the event handlers to the required elements.
   * 
   * It can accept an options object (detailed in Ajaxify.process)
   * 
   * @param options object See Ajaxify.process
   * @return object The jQuery object
   * @author Dom Hastings
   */
  $.fn.ajaxify = function(options) {
    options = $.extend({}, Ajaxify.options, options || {});

    // loop through all the matched elements
    for (var i = 0; i < this.length; i++) {
      $(this[i]).data('options', options);

      // if we're dealing with a link
      if ($(this[i]).attr('tagName').toLowerCase() == 'a') {
        // just bind to the click event
        $(this[i]).bind('click', function(event) {
          event.preventDefault();

          if (!$(this).data('options').confirm || ($(this).data('options').confirm && confirm($(this).data('options').confirm))) {
            // process the event
            Ajaxify.process(event, this);
          }
        });

      // if it's a form
      } else if ($(this[i]).attr('tagName').toLowerCase() == 'form') {
        // find the possible submission methods
        $(this[i]).find(options.buttons).each(function(i, e) {
          // and attach click handlers to each
          $(e).click(function(event) {
            $(this).before('<input type="hidden" name="' + $(this).attr('name') + '" value="' + $(this).val() + '" class="ajaxify__submitButton__"/>').attr('name', $(this).attr('name')).val($(this).val());

            // if it's an imagae, also capture the x/y co-ordinates
            if ($(this).attr('type') == 'image') {
              $(this).before('<input type="hidden" name="' + $(this).attr('name') + '_y" value="' + (event.pageY - $(this).offset().top) + '" class="ajaxify__submitButtonX__"/>');
              $(this).before('<input type="hidden" name="' + $(this).attr('name') + '_x" value="' + (event.pageX - $(this).offset().left) + '" class="ajaxify__submitButtonY__"/>');
            }
          });
        });

        // bind to the submit event
        $(this[i]).bind('submit', function(event) {
          event.preventDefault();

          if (!$(this).data('options').confirm || ($(this).data('options').confirm && confirm($(this).data('options').confirm))) {
            // process the event
            Ajaxify.process(event, this);
          }
        });
      }
    }

    // return the jQuery object for chaining
    return this;
  }
})(jQuery);

/**
 * Ajaxify
 * 
 * The main logic object.
 * 
 * @package jquery.ajaxify
 * @author Dom Hastings
 */
var Ajaxify = {
  /**
   * options
   * 
   * @var object Which may contain the following keys:
   *   'append': A query string to append to the URL (can help to treat AJAX requests differently, default is: ajax=1)
   *   'buttons': A jQuery selector of the what is classed as a button (default: button[type=submit], input[type=submit], input[type=image])
   *   'confirm': When set to a string when the link/button is clicked a confirm() box will be displayed and the script will only proceed if Ok is pressed
   *   'replace': When set to true the new content will replace all content in the element specified by 'update', otherwise just appends
   *   'submit': Submit options:
   *     'disable': If the selector is set, all child elements of the main element that match the selector will be set to disabled. The selector key can be set to 'buttons' to use the buttons selector. If className is specified, this will be applied using jQuery.addClass()
   *     'message': If the text is set, a <div/> will be created containing the specified text when the request starts. If className is specified, this will be applied using jQuery.addClass()
   *     'waiting': If the timeout is specified then after timeout * 1000 ms, the script will optionally re-enable the submit buttons if they were previously disabled, update the message displayed to the specified message key value (if not empty), applying the specified className using jQuery.addClass()
   *   'update': A jQuery selector of an element to update with the result (default: element.target or element parent if not specified)
   *   Also accepts any of the jQuery AjaxOptions keys (http://docs.jquery.com/Ajax/jQuery.ajax#options)
   */
  options: {
    'append': 'ajax=1',
    'buttons': 'button[type=submit], input[type=submit], input[type=image]',
    'confirm': null,  // if set to text, will be displayed in a confirm() box before proceeding
    'replace': true,  // if set to true, will replace content in the update element, otherwise will just append
    'submit': { // events to be carried out onclick/submit
      'disable': {  // disable any inputs (form only)
        'selector': null,
        'className': null
      },
      'message': {  // display a message when the click event is fired
        'text': null,
        'className': null
      },
      'waiting': { // if nothing happens after timeout * 1000 ms, update the message and re-enable the buttons
        'timeout': 0, // seconds
        'message': null,
        'className': null,
        'callback': null  // callback to display an alternative message to users after the specified period
      }
    },
    'update': null,
    // jQuery AJAX options, see http://docs.jquery.com/Ajax/jQuery.ajax#toptions
    'async': true,
    'beforeSend': null,
    'complete': null,
    'contentType': null,
    'dataFilter': null,
    'dataType': 'html',
    'error': function(XHR, textStatus, errorThrown) {
      // to access the options you can use var options = this; or see the success function for alternative is this changes in future
      if ('console' in window) {
        if ('warn' in window.console) {
          console.warn('Error processing data via AJAX:\n' + errorThrown + ' (' + textStatus + ')');

        } else if ('log' in window.console) {
          console.log('Warning: Error processing data via AJAX:\n' + errorThrown + ' (' + textStatus + ')');
        }

      } else {
        alert('Error processing data via AJAX:\n' + errorThrown + ' (' + textStatus + ')');
      }
    },
    'success': function(data, textStatus) {
      // this refers to this options object, when I assumed it would refer to the AJAX object, will this change in future versions?
      var options = this;
      // if it does change in the future, then this snippet should help:
      // if (this.id) {
      //   var options = Ajaxify.retrieve(this.id).options;
      // }

      if (options.replace) {
        ////  THIS SECTION CHANGED BY CHRISTOPHER:  //
        if (options.replace == true) {              //
            jQuery(options.update).html(data);      //
        } else {                                    //
            options.replace(data, options);         //
        }                                           //
      } else {                    
        jQuery(options.update).append(data);
      }
    },
    'type': null,
    'url': null
  },

  /**
   * data
   * 
   * Stores the data for each request
   * 
   * @var array
   */
  data: [],

  /**
   * store
   * 
   * Stores the request data
   * 
   * @param data mixed The data to store
   * @return integer The array key for the request
   * @author Dom Hastings
   */
  store: function(data) {
    var k = this.data.length;

    this.data.push(data);

    return k;
  },

  /**
   * retrieve
   * 
   * Retrieves the request data
   * 
   * @param k integer The data key
   * @return mixed The data stored
   * @author Dom Hastings
   */
  retrieve: function(k) {
    if (this.data[k]) {
      return this.data[k];

    } else {
      // throw new Error('Ajaxify.retrieve: Unknown key: "' + k '"');
      return;
    }
  },

  /**
   * process
   * 
   * The main function called by the jQuery function
   * 
   * @param e object The jQuery event object
   * @param node object The node being processed
   * @return string The request body
   * @author Dom Hastings
   */
  process: function(e, node) {
    var $ = jQuery;

    // initialize the options object
    var options = {};

    // extend the object with the default options
    $.extend(options, $(node).data('options'));

    // if we're working on a form
    if ($(node).attr('tagName').toLowerCase() == 'form') {
      // set the url to the action attribute or the options url if specified on init
      options.url = (options.url) ? this.appendToURL(options.url, options.append) : this.appendToURL($(node).attr('action'), options.append);
      // set the type to the method attribute or the options type
      options.type = (options.type) ? options.type : $(node).attr('method').toUpperCase();
      // set the content type
      options.contentType = (options.contentType) ? options.contentType : $(node).attr('enctype') || 'application/x-www-form-urlencoded';
      // get the form data
      if (options.data) {
        if (typeof options.data == 'string') {
          options.data = $(node).serialize() + '&' + options.data;

        } else {
          options.data = $(node).serialize() + '&' + $.param(options.data);
        }

      } else {
        options.data = $(node).serialize();
      }

    // if we're working on a link
    } else if ($(node).attr('tagName').toLowerCase() == 'a') {
      // set the url to the href attribute or the options url if specified
      options.url = (options.url) ? this.appendToURL(options.url, options.append) : this.appendToURL($(node).attr('href'), options.append);
      // set the type to GET or the options type
      options.type = (options.type) ? options.type : 'GET';
      // set the content type
      options.contentType = (options.contentType) ? options.contentType : 'application/x-www-form-urlencoded';

    // if it's not a form or a link leave it alone!
    } else {
      return;
    }

    // Make sure we have an id
    if ($(node).attr('id')) {
      var id = $(node).attr('id');

    } else {
      var id = 'ajaxify__unique__' + this.data.length;

      $(node).attr('id', id);
    }

    // Build the selector for the element
    var selector = $(node).attr('tagName').toLowerCase() + '#' + id;

    // update the element specified in options, or the parent element if not
    options.update = (options.update) ? options.update : ($(node).attr('target') ? $(node).attr('target') : $(node).parent());

    // submit events
    if ($(node).attr('tagName').toLowerCase() == 'form') {
      if (options.submit.disable.selector) {
        // if the selector is set to 'buttons'
        if (options.submit.disable.selector == 'buttons') {
          // use the options.buttons selector
          options.submit.disable.selector = options.buttons;
        }

        // find all the buttons
        $(node).find(options.submit.disable.selector).each(function(i, e) {
          // set the class, if it's specified
          if (options.submit.disable.className) {
            $(e).addClass(options.submit.disable.className);
          }

          $(e).attr('disabled', true);
        });
      }

    } else {
      // if it's not a form
      if (options.submit.disable.selector) {
        // disable the selector, we can't use it anyway
        options.submit.disable.selector = null;
      }
    }

    // check for adding a message
    if (options.submit.message.text) {
      if ($('div#ajaxify__submitMessage__').length == 0) {
        $('body').append($('<div id="ajaxify__submitMessage__"></div>'));
      }

      $('div#ajaxify__submitMessage__').html(options.submit.message.text);

      if (options.submit.message.className) {
        $('div#ajaxify__submitMessage__').addClass(options.submit.message.className);
      }
    }

    // move the complete callback because we need ours to run
    if (options.complete) {
      options.onComplete = options.complete;
    }

    // move the beforeSend callback because we need ours to run
    if (options.beforeSend) {
      options.onBeforeSend = options.beforeSend;
    }

    options.complete = function(XHR, textStatus) {
      if ('id' in this) {
        var data = Ajaxify.retrieve(this.id);

      } else {
        var data = false;
      }
      
      if (data) {
        // clear the timeout
        if (data.timeout) {
          window.clearTimeout(data.timeout);
        }

        // get rid of the placeholders
        $(data.selector).find('input.ajaxify__submitButton__, input.ajaxify__submitButtonX__, input.ajaxify__submitButtonY__').remove();

        // if we disabled the buttons, re-enable them
        if (data.options.submit.disable.selector) {
          var els = $(data.selector).find(data.options.submit.disable.selector).each(function(i, e) {
            if (data.options.submit.disable.className) {
              $(e).removeClass(data.options.submit.disable.className);
            }

            $(e).attr('disabled', false);
          });
        }

        // if the onComplete callback is set, run it
        if (data.options.onComplete) {
          // ...well, try to
          try {
            data.options.onComplete(XHR, textStatus);
          // fail silently
          } catch (e) {}
        }
      }
      
      // clear the message if it's set
      if ($('div#ajaxify__submitMessage__').length) {
        $('div#ajaxify__submitMessage__').fadeOut(600, function() {
          $(this).remove();
        });
      }
    }

    // if we're cleaning up after ourselves
    if (options.submit.waiting.timeout) {
      // yuck. can this be done differently?
      eval('var f = function() { Ajaxify.cleanUp(' + this.data.length + '); };');

      // store the timeout too
      options.timeout = window.setTimeout(f, (options.submit.waiting.timeout * 1000));

    } else {
      options.timeout = null;
    }
    
    options.id = Ajaxify.store({
      'selector': selector,
      'options': options,
      'timeout': options.timeout
    });

    // run the request
    $.ajax(options);
  },

  /**
   * cleanUp
   * 
   * The function called if the request has been running for a while
   * 
   * @param id integer The key in Ajaxify.data[] where the data for this request is stored
   * @return string The request body
   * @author Dom Hastings
   */
  cleanUp: function(id) {
    // ease of use
    var $ = jQuery;

    // load the data
    var data = Ajaxify.retrieve(id);

    // check we have some, else return
    if (!data) {
      return;
    }

    // if the selector is set
    if (data.options.submit.disable.selector) {
      // find them all
      $(data.selector).find(data.options.submit.disable.selector).each(function(i, e) {
        // if theres a new class
        if (data.options.submit.disable.className) {
          // set it
          $(e).addClass(data.options.submit.disable.className);
        }

        // enable it again
        $(e).attr('disabled', false);
      });
    }

    // change the message
    if (data.options.submit.waiting.message) {
      $('div#ajaxify__submitMessage__').html(data.options.submit.waiting.message);
    }

    // apply the updated class
    if (data.options.submit.waiting.className) {
      $('div#ajaxify__submitMessage__').addClass(data.options.submit.waiting.className);
    }

    // fire the custom callback
    if (data.options.submit.waiting.callback) {
      // try and call it
      try {
        data.options.submit.waiting.callback();
      // fail silently
      } catch (e) {}
    }
  },

  /**
   * appendToURL
   * 
   * Appends the specified query string to the URL being requested
   * 
   * @param url string The URL being requested
   * @return string The URL with the query string appended if specified
   * @author Dom Hastings
   */
  appendToURL: function(url, append) {
    // if the options specify a URL append
    if (append) {
      // if there's a # in the url, strip it off first
      if (url.indexOf('#') != -1) {
        url = url.substr(0, url.indexOf('#'));
      }

      // add it correctly (using & if ? already appears in the URL)
      url += (url.indexOf('?') == -1 ? '?' + append : '&' + append)
    }

    return url;
  }
}
