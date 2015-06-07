import argparse
import tractdb.admin
import yaml

if __name__ == '__main__':
    # Parse our command line
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--file',
        '-f',
        dest='file_config',
        required=True,
        help='Path to config file'
    )
    args = parser.parse_args()

    # Recover what we need  
    file_config = args.file_config

    # Load our config file
    with open(file_config) as f:
        config = yaml.safe_load(f)

    # Create our admin object
    admin = tractdb.admin.TractDBAdmin(
        server_url=config['server_url'],
        server_admin=config['server_admin'],
        server_password=config['server_password']
    )

    # Do some simple manipulation of the server
    print(admin.list_users())
    admin.create_user('test1', 'test1pass')
    print(admin.list_users())
    admin.delete_user('test1')
    print(admin.list_users())
