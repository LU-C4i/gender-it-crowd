# gender-it-crowd
Gender-IT is a small and simple website that allows crowd classification. 
For an example click: http://genderit.peaceinformaticslab.org/
  
# Prerequisites

* Python 2.7
* Virtualenv
* pip
	
# UBUNTU INSTALLATION Prerequisites 

	sudo apt-get install python-setuptools
	sudo apt-get install build-essential python-dev \
	    libsqlite3-dev libreadline6-dev \
	    libgdbm-dev zlib1g-dev libbz2-dev \
	    sqlite3 zip libmysqlclient-dev libffi-dev 
	sudo apt-get install pip virtualenv
	
# Installation
	
1. Fill in the database settings in the webserver.cfg, e.g.:

    user = [username]
    password = [password_user]
    host = [ipadres_server]
    port = 3306
    default_db = [db_name]

2. Execute the following commands:

    virtualenv venv
    source venv/bin/activate		
    pip install -r requirements.txt
    
3. Execute the sql code in `schema.sql` in order to create the correct tables and procedures
4. Take your twitter data and fill it in into the t_tus_twitter table. Description of the columns are:
    * `tus_id`, is auto increment
    * `tus_twitter_user_id`, the twitter id of the user
    * `tus_screenname`, screenname of the twitter user
    * `tus_name`, name of the twitter user
    * `tus_description`, description of the twitter user
    * `tus_picture_url`, url of the profile picture
    * `tus_last_tweet`, the text of the last tweet of the user		
		
# Run website

1. Activate the virtual environment

    source venv/bin/activate		
    
2. Run the website

    make run
    
3. Browse to: http://localhost:8080

# Getting the results

A result only counts if 3 users have the same prediction. 
Run the `p_cpf_crowdprediction_final_refresh` procedure to fill the `t_ppf_crowdprediction_final` tabel with the
final results.
