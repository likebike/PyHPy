
dev:
	@python ${HOME}/Makefile.py dev

prod:
	@python ${HOME}/Makefile.py prod

fast:
	@ACL_CHECK=0 python ${HOME}/Makefile.py dev

