from flask import render_template, request, session, redirect


def get_bvo_id():
    return session.get('id')


def get_team_selection():
    return request.values.get('teamSelectie', "Onder 13")


def vertesprong():
    bvo_id = get_bvo_id()

    if (bvo_id == None):
        return redirect('/login')

    header = "Vertesprong"
    template_location = 'dashboard/verspringen.html'
    return render_template(template_location, header=header)


def sprint():
    bvo_id = get_bvo_id()

    if (bvo_id == None):
        return redirect('/login')

    header = "Sprint per afstand"
    template_location = 'dashboard/sprint.html'
    return render_template(template_location, header=header)


def change_of_direction():
    bvo_id = get_bvo_id()

    if (bvo_id == None):
        return redirect('/login')

    header = "CoD Scores per been"
    template_location = 'dashboard/cod.html'
    return render_template(template_location, header=header)


def algemene_motoriek():
    bvo_id = get_bvo_id()

    if (bvo_id == None):
        return redirect('/login')

    header = "Algemene Motoriek"
    template_location = 'dashboard/algemene_motoriek.html'
    return render_template(template_location, header=header)
