dumpdata:
	python src/manage.py dumpdata --indent 4 members.User > src/fixtures/users.json
	python scripts/create_groups_fixture.py

loaddata:
	python src/manage.py loaddata src/fixtures/groups.json
	python src/manage.py loaddata src/fixtures/users.json
	python src/manage.py loaddata src/fixtures/positions.json

rebuild_migrations:
	echo **/migrations/*.py | sed 's/ /\n/g' | grep -v '__' | xargs rm -f
	rm -f src/system/db.sqlite3
	python src/manage.py makemigrations
	python src/manage.py migrate
	$(MAKE) loaddata

