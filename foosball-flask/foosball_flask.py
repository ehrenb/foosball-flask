"""Foosball TrueSkill Server

This server ranks foosball players and teams using the TrueSkill ranking
algorithm.

"""

import flask
import logging
import logging.config
import traceback
import sys

import utils.data_manager as data_manager
import utils.data_manager_exceptions as data_manager_exceptions
import utils.foosball_exceptions as foosball_exceptions

try:
    logging.config.fileConfig("./utils/logging.conf",
        disable_existing_loggers=False)
    LOGGER = logging.getLogger("foosball")
except IOError:
    traceback.print_exc()
    sys.exit("Aborting. Unable to find foosball log config")
else:
    pass

FOOSBALL_APP = flask.Flask(__name__, static_folder='./utils/static',
    template_folder='./utils/templates')

FOOSBALL_APP.config['DEBUG'] = True

FOOSBALL_DATA = data_manager.DataManager(db_user='foosball',
    db_pass='foosball', db_host='127.0.0.1', db_name='foosball')

@FOOSBALL_APP.route('/')
def index_redirect():
    """Main entry point to webpage

    Args:
        None

    Returns:
        display dashboard

    """

    player_count = FOOSBALL_DATA.get_total_players()
    team_count = FOOSBALL_DATA.get_total_teams()

    return flask.render_template('dashboard.html', player_count=player_count,
        team_count=team_count)

@FOOSBALL_APP.route('/index')
def index():
    """Dashboard webpage

    Args:
        None

    Returns:
        display dashboard

    """

    player_count = FOOSBALL_DATA.get_total_players()
    team_count = FOOSBALL_DATA.get_total_teams()

    return flask.render_template('dashboard.html', player_count=player_count,
        team_count=team_count)

@FOOSBALL_APP.route('/result')
def result():
    """Results webpage

    Args:
        None

    Returns:
        display results

    """

    return flask.render_template('result.html')

@FOOSBALL_APP.route('/player')
def player():
    """Players webpage

    Args:
        None

    Returns:
        display players

    """

    players = FOOSBALL_DATA.get_all_players()

    return flask.render_template('player.html', players=players)

@FOOSBALL_APP.route('/team')
def team():
    """Team webpage

    Args:
        None

    Returns:
        display teams

    """

    return flask.render_template('team.html')

@FOOSBALL_APP.route('/addteam')
def add_team():
    """Add Team webpage

    Args:
        None

    Returns:
        display add team

    """

    return flask.render_template('addteam.html')

@FOOSBALL_APP.route('/addplayer', methods=['GET', 'POST'])
def add_player():
    """Add Player webpage

    Args:
        first_name (str):   player first name
        last_name (str):    player last name
        nickname (str):     player nickname

    Returns:
        display add player
        display player

    Raises:
        foosball_exceptions.HTTPError

    """

    if flask.request.method == 'POST':
        first_name = flask.request.form['first_name']
        last_name = flask.request.form['last_name']
        nickname = flask.request.form['nickname']

        try:
            FOOSBALL_DATA.add_player(first_name=first_name,
                last_name=last_name, nickname=nickname)
            FOOSBALL_DATA.commit_data()
        except data_manager_exceptions.DBValueError as error:
            LOGGER.error(error.msg)
            return flask.render_template('addplayer.html', error=error)
        except data_manager_exceptions.DBSyntaxError as error:
            LOGGER.error(error.msg)
            return flask.render_template('addplayer.html', error=error)
        except data_manager_exceptions.DBConnectionError as error:
            LOGGER.error(error.msg)
            return flask.render_template('addplayer.html', error=error)
        except data_manager_exceptions.DBExistError as error:
            LOGGER.error(error.msg)
            return flask.render_template('addplayer.html', error=error)
        else:
            pass

        message = 'Player successfully added'
        players = FOOSBALL_DATA.get_all_players()
        return flask.render_template('player.html', message=message,
            players=players)
    elif flask.request.method == 'GET':
        return flask.render_template('addplayer.html')
    else:
        raise foosball_exceptions.HTTPError("Received unrecognized HTTP method")

@FOOSBALL_APP.route('/delplayer', methods=['GET'])
def del_player():
    """Delete player webpage

    Args:
        first_name (str):   player first name
        last_name (str):    player last name
        nickname (str):     player nickname

    Returns:
        display player

    Raises:
        foosball_exceptions.HTTPError

    """

    if flask.request.method == 'GET':
        first_name = flask.request.args.get('first_name').encode('utf-8')
        last_name = flask.request.args.get('last_name').encode('utf-8')
        nickname = flask.request.args.get('nickname').encode('utf-8')

        try:
            FOOSBALL_DATA.delete_player(first_name=first_name,
                last_name=last_name, nickname=nickname)
            FOOSBALL_DATA.commit_data()
        except data_manager_exceptions.DBValueError as error:
            LOGGER.error(error.msg)
            return flask.render_template('player.html', error=error)
        except data_manager_exceptions.DBSyntaxError as error:
            LOGGER.error(error.msg)
            return flask.render_template('player.html', error=error)
        except data_manager_exceptions.DBConnectionError as error:
            LOGGER.error(error.msg)
            return flask.render_template('player.html', error=error)
        except data_manager_exceptions.DBExistError as error:
            LOGGER.error(error.msg)
            return flask.render_template('player.html', error=error)
        else:
            pass

        message = 'Player successfully deleted'
        players = FOOSBALL_DATA.get_all_players()
        return flask.render_template('player.html', message=message,
            players=players)

    else:
        raise foosball_exceptions.HTTPError("Received unrecognized HTTP method")

@FOOSBALL_APP.route('/addresult')
def add_result():
    """Add Result webpage

    Args:
        None

    Returns:
        display add result

    """

    return flask.render_template('addresult.html')

@FOOSBALL_APP.route('/teamstat')
def team_stat():
    """Team Stat webpage

    Args:
        None

    Returns:
        display dashboard

    """

    player_count = FOOSBALL_DATA.get_total_players()
    team_count = FOOSBALL_DATA.get_total_teams()

    return flask.render_template('dashboard.html', player_count=player_count,
        team_count=team_count)

@FOOSBALL_APP.route('/playerstat')
def player_stat():
    """Player Stat webpage

    Args:
        None

    Returns:
        display dashboard

    """

    player_count = FOOSBALL_DATA.get_total_players()
    team_count = FOOSBALL_DATA.get_total_teams()

    return flask.render_template('dashboard.html', player_count=player_count,
        team_count=team_count)

def main():
    """Main entry point

    Args:
        None

    Returns:
        None

    """

    FOOSBALL_APP.run(port=11111, host='0.0.0.0')

if __name__ == '__main__':
    main()
