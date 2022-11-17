from flask import render_template, request, session, redirect
from visualisation import scatterplot, cod
from visualisation import handcorplot
from visualisation import sprintplot
from database import database

def get_bvo_id():
    return session.get('id')


def get_team_selection():
    return request.values.get('teamSelectie', "Onder 13")


def vertesprong():
    bvo_id = get_bvo_id()
    team_selection = get_team_selection()

    if (bvo_id == None):
        return redirect('/login')

    result = database.request_vertesprong(team_selection, bvo_id)
    graphJSON = scatterplot.vertesprong(result)
    header = "Vertesprong"
    description = f"Resultaten van de vertesprong voor de groep {team_selection} jaar. "
    template_location = 'dashboard/verspringen.html'

    return render_template(template_location, graphJSON=graphJSON, header=header, description=description)


def sprint():
    bvo_id = get_bvo_id()
    team_selection = get_team_selection()

    if (bvo_id == None):
        return redirect('/login')

    result = database.request_sprint(bvo_id)
    graphJSON = sprintplot.sprint(result)
    header = "Sprint per afstand"
    description = f"Resultaten van de 10,20 en 30 meter sprint . "
    template_location = 'dashboard/sprint.html'

    return render_template(template_location, graphJSON=graphJSON, header=header, description=description)


def hand_oog_coordinatie():
    bvo_id = get_bvo_id()

    if (bvo_id == None):
        return redirect('/login')

    result = database.request_hand_oog_coordinatie(bvo_id)
    graphJSON = handcorplot.hand_oog_coordinatie(result)
    header = "Hand-Oog Coordinatie"
    description = f"Resultaten van de hand-oog coordinatie"
    template_location = 'dashboard/handoogcoordinatie.html'

    return render_template(template_location, graphJSON=graphJSON, header=header, description=description)


def evenwichtsbalk_showcase():
    bvo_id = get_bvo_id()

    if (bvo_id == None):
        return redirect('/login')
        
    header = "Evenwichtsbalk"
    template_location = 'dashboard/evenwichtsbalk_showcase_2.html'

    return render_template(template_location, header=header)   


def zijwaarts_verplaatsen():
    bvo_id = get_bvo_id()
    team_selection = get_team_selection()

    if (bvo_id == None):
        return redirect('/login')

    result = database.request_zijwaarts_verplaatsen(team_selection, bvo_id)
    graphJSON = scatterplot.zijwaarts_verplaatsen(result)
    header = "Zijwaarts Verplaatsen"
    description = f"Resultaten van het zijwaarts verplaatsen voor de groep {team_selection} jaar. "
    template_location = 'dashboard/zijwaartsverplaatsen.html'

    return render_template(template_location, graphJSON=graphJSON, header=header, description=description)


def zijwaarts_springen():
    bvo_id = get_bvo_id()

    if bvo_id is None:
        return redirect('/login')

    header = "Zijwaarts Springen"
    template_location = 'dashboard/zijwaartsspringen.html'

    return render_template(template_location, header=header)


def change_of_direction():
    bvo_id = get_bvo_id()
    team_selection = get_team_selection()

    if (bvo_id == None):
        return redirect('/login')

    result = database.request_change_of_direction(team_selection, bvo_id)
    graphJSON = cod.change_of_direction(result)
    header = "CoD Scores per been"
    description = f"Resultaten van de CoD voor alle teams. "
    template_location = 'dashboard/cod.html'

    return render_template(template_location, graphJSON=graphJSON, header=header, description=description)


def algemene_moteriek():
    bvo_id = get_bvo_id()

    if (bvo_id == None):
        return redirect('/login')

    header = "Algemene Moteriek"
    template_location = 'dashboard/algemene_moteriek.html'

    return render_template(template_location, header=header)
