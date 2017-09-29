"""
Fabfile encapsulating both the server and client fabfiles of opentaba since they now both reside
in the server repository
"""

from fabric.api import prompt, task


from scripts.client_fabfile import create_client, update_client_social_links

from scripts.server_fabfile import create_server, delete_server, update_gushim_server, deploy_server, deploy_server_all, create_db
from scripts.server_fabfile import update_db, scrape, renew_db, renew_db_all, refresh_db, refresh_db_all, set_poster, sync_poster
from scripts.server_fabfile import fix_mmi_links

from scripts.poster_fabfile import add_new_poster


@task
def create_municipality(muni_name, display_name):
    """Run both server and client creation tasks automatically"""
    
    print 'This task is not recommended for use as it is too automatic. We advise you '
    print 'to follow the instructions found in DEPLOYMENT.md instead.'
    
    sure = ''
    while sure not in ['yes', 'no']:
        sure = prompt('Are you sure you want to use this task (yes/no) ?')
    
    if sure == 'yes':
        create_server(muni_name, display_name)
        create_client(muni_name, display_name)


@task
def create_poster(muni_name, poster_app_name, poster_desc='', fb_app_id=None, fb_app_secret=None, tw_con_id=None, tw_con_secret=None, fb_link='', tw_link=''):
    """Create a new poster document on the poster server and set the needed environment variables on the opentaba-server instance"""
    
    poster_id = add_new_poster(poster_app_name, poster_desc, fb_app_id, fb_app_secret, tw_con_id, tw_con_secret)
    set_poster(muni_name, 'http://%s.herokuapp.com/' % poster_app_name, poster_id)
    
    if len(fb_link) > 0 or len(tw_link) > 0:
        update_client_social_links(muni_name, fb_link, tw_link)
    
    print '*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*'
    print 'Done creating a new poster and setting the environment variables on the'
    print 'opentaba-server! If not alreadey set, you can set links to the Facebook'
    print 'and Twitter pages that will appear on the website using the'
    print 'update_client_social_links task'
    print '*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*'
