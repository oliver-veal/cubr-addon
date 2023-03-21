import bpy

from .. import props


def refresh_token_timer():
    print("Cubr: Refreshing token")

    try:
        r = props.api().refresh_token(props.auth().refresh_token)

        if r.status_code != 200:
            print("Cubr: Failed to refresh token: Status code " + str(r.status_code))
            print(r.text)
            props.auth().logout()
            return

        res = r.json()

        props.auth().login(res['access_token'], res['refresh_token'], 0)

        print("Cubr: Refreshed token")

        return res['expires_in'] - 5 * 60
    except Exception as e:
        print("Cubr: Failed to refresh token")
        print(e)
        props.auth().logout()
        return


def poll_login():
    if props.props().login_session_token == "":
        bpy.app.timers.unregister(poll_login)
        return None

    r = props.api().get('/addon/get_login_session?session_id=' +
                        props.props().login_session_token)

    if r.status_code != 200:
        return None

    res = r.json()

    if res['expired'] == True or res['denied'] == True:
        print("Cubr: Login session expired or denied")
        props.auth().clearLoginSession()
        bpy.app.timers.unregister(poll_login)

        return None

    if res['access_token'] != "" and res['refresh_token'] != "":
        print("Cubr: Logged in")

        props.auth().clearLoginSession()
        props.auth().login(
            res['access_token'],
            res['refresh_token'],
            res['expires_at']
        )

        bpy.app.timers.unregister(poll_login)

        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()

        return None

    return 1
