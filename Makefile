
dev:
	python ${HOME}/bin/create_app_pages.py
	python ${HOME}/bin/publish_to_www.py dev

prod:
	python ${HOME}/bin/create_app_pages.py
	python ${HOME}/bin/publish_to_www.py prod

fast:
	python ${HOME}/bin/create_app_pages.py
	ACL_CHECK=0 python ${HOME}/bin/publish_to_www.py dev

