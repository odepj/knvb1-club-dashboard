Projectvoortgang KNVB-2.

In september begonnen wij als groepje met ons Big Data project voor de KNVB. Dit project startte met een meeting met de KNVB waarin het volgende werd verteld.
Wij zijn het tweede team studenten van de HvA die aan deze opdracht hebben gewerkt. Deze opdracht gaat over de talentenmonitor van de KNVB. Talentenmonitor:  inzicht voor jeugdopleidingen in de ontwikkeling van hun spelers. Ons vorige groepje heeft een basis dashboard achtergelaten waarin te zien is hoe bepaalde jeugdteams scoren op verschillende categorieën. 

Als feedback op het huidige dashboard hadden we meegekregen dat bepaalde X en Y assen moeten worden aangepast en een paar vaardigheid grafieken moeten worden toegevoegd. 

Verder moeten we gemiddeldes, medianen en benchmark resultaten toevoegen aan grafieken en deze optimaliseren. Hierin kunnen clubs dan zien wat hun teams scoren en daarmee nieuwe inzichten krijgen.  Ons doel daarin is deze inzichten zo goed mogelijk visualiseren en de back end zo netjes mogelijk maken. Deze genoemde back end was aan het begin van het project namelijk zeer rommelig en onoverzichtelijk.
Dit zal ervoor zorgen dat elke club de juiste data te zien krijgt, rechten heeft en de 
KNVB een admin account zal hebben met gevraagde bevoegdheden.
Verder moet het dashboard ook nog mobile responsive worden.

Aan het einde van sprint 1 hadden we het volgende gedaan:
-	CSV bestand ontvangen met gegenereerde data -> verwerkt met Pandas -> Database opgezet met SqlAlchemy ORM.
-	Docker & CI/CD pipeline.
-	Analyses gedaan voor machine learning, webscraping.
Aan het einde van sprint 2 hadden we het volgende gedaan:
-	Refactoring van de applicatie.
-	Registratie authenticatie.
-	Eerste schetsen van datavisualisatie.
Aan het einde van sprint 3 hadden we het volgende gedaan:
-	Meeting gehad bij KNVB met onze voortgang
-	Zeven verschillende visualisaties laten zien aan de KNVB om uit te kiezen.
-	Feedback KNVB verwerkt
Aan het einde van sprint 4 hadden we het volgende gedaan:
-	Splitsing KNVB teams waarbij ons team het volgende moest af hebben: Dashboard template in Dash, Per club, code gegenereerd beter onderhoudbaar en leesbaar, meer verschillende grafieken onder de verschillende tegels.
-	Dash dashboard template gemaakt.
-	Nieuwe dataset geïmplenteerd.
-	Nieuw eindresultaat: Demo app van 1 club in Docker, App voor de KNVB in Docker, Database connectie string die veranderd kan worden.
Aan het einde van sprint 5 hadden we het volgende gedaan:
-	Dashboard geoptimaliseerd.
-	Bug fixes.
-	Code clean up.
-	Database connectie met de KNVB.
-	SQL-files geëxporteerd. 
-	Eindproduct af.
-	Usecase van het project.

Aan het einde van het project hebben we een bruikbaar product gemaakt voor de KNVB die aan de eisen voldoet die vooraf gesteld zijn. Dit houdt in dat we een template hebben gemaakt voor elke tegel (vaardigheid) waarin de scores worden gemeten van de teams. Deze scores kunnen gezien worden in een boxplot, lijngrafiek of BLOC-test. Ook hebben we filters gemaakt zodat de gebruiker makkelijk kan selecteren op zijn of haar wensen. Deze filters zijn: gemiddelde, boxplot, mediaan en individuele datapunten. Ook kan de gebruiker nog filteren op lichting, team of seizoen. De back end is ook geoptimaliseerd en direct bruikbaar voor het volgende groepje. De visuele uitkomst van ons product zullen we presenteren in de oplevering van sprint 5 en tijdens Digital Creators op donderdag 26 januari.
