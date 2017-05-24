from project import  project
v = project("/tmp/pr/prj.txt",
            "/tmp/pr/",
            443,
            "https",
            2,
            "/tmp/pr/db.db",
            2,
            "desktop",
            "/usr/local/bin/phantomjs",
            "/tmp/pr/screen.js"
            )
v.save_to_db = True
v.start()