-- Create a new table called 'bvo' in schema 'ztiggele'
CREATE TABLE IF NOT EXISTS ztiggele.bvo
(
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `bvo_naam`NVARCHAR(50) NOT NULL UNIQUE,
    `bvo_jeugdopleiding` NVARCHAR(50)
);

-- Create a new table called 'team' in schema 'ztiggele'
CREATE TABLE IF NOT EXISTS ztiggele.team
(
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `team_naam` NVARCHAR(25) NOT NULL UNIQUE
);

-- Create a new table called 'reeks' in schema 'ztiggele'
CREATE TABLE IF NOT EXISTS ztiggele.reeks
(
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `seizoen` NVARCHAR(10) NOT NULL,
    `reeks_naam` NVARCHAR(10) NOT NULL,
	`jaar` DECIMAL(4,0) NOT NULL,
    UNIQUE INDEX ix_reeks_naam_jaar (reeks_naam, jaar)
);

-- Create a new table called 'speler' in schema 'ztiggele'
CREATE TABLE IF NOT EXISTS ztiggele.speler
(
    `id` NVARCHAR(7) NOT NULL PRIMARY KEY,
    `geboortedatum` DATE,
    `gender` NVARCHAR(1),
    `toestemming` BIT NOT NULL
);

-- Create a new table called 'allocatie' in schema 'ztiggele'
CREATE TABLE IF NOT EXISTS ztiggele.allocatie
(
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `bvo_id` INT NOT NULL,
    `team_id` INT NOT NULL,
    `reeks_id` INT NOT NULL, 
    `speler_id` NVARCHAR(7) NOT NULL,
    INDEX ix_bvo_team_reeks (bvo_id, team_id, reeks_id),
    UNIQUE INDEX ix_reeks_speler (reeks_id, speler_id), 
	FOREIGN KEY (id) REFERENCES bvo(id),
	FOREIGN KEY (id) REFERENCES team(id),
	FOREIGN KEY (id) REFERENCES reeks(id),
	FOREIGN KEY (id) REFERENCES speler(id)

);

-- Create a new table called 'han' in schema 'ztiggele'
CREATE TABLE IF NOT EXISTS ztiggele.han
(
    `allocatie_id` INT NOT NULL PRIMARY KEY,
	`Testdatum` DATE,
    `Staande lengte` DECIMAL(4,1),
	`Zittende lengte` DECIMAL(4,1),
	`Lengte bovenlichaam` DECIMAL(4,1),
	`Gewicht` DECIMAL(4,1),
	`Maturity Offset` DECIMAL(4,2),
	`Balance Beam 6cm` DECIMAL(3,0),
	`Balance Beam 4.5cm` DECIMAL(3,0),
	`Balance Beam 3cm` DECIMAL(3,0),
	`Balance beam totaal` DECIMAL(3,0),
	`Zijwaarts springen 1` DECIMAL(3,0),
	`Zijwaarts springen 2` DECIMAL(3,0),
	`Zijwaarts springen totaal` DECIMAL(3,0),
	`Zijwaarts verplaatsen 1` DECIMAL(3,0),
	`Zijwaarts verplaatsen 2` DECIMAL(3,0),
	`Zijwaarts verplaatsen totaal` DECIMAL(3,0),
	`Oog-hand coordinatie 1` DECIMAL(3,0),
	`Oog-hand coordinatie 2` DECIMAL(3,0),
	`Oog-hand coordinatie Totaal` DECIMAL(3,0),
	`10 meter sprint 1` DECIMAL(5,3),
	`10 meter sprint 2` DECIMAL(5,3),
	`10 meter sprint beste` DECIMAL(5,3),
	`20 meter sprint 1` DECIMAL(5,3),
	`20 meter sprint 2` DECIMAL(5,3),
	`20 meter sprint beste` DECIMAL(5,3),
	`30 meter sprint 1` DECIMAL(5,3),
	`30 meter sprint 2` DECIMAL(5,3),
	`30 meter sprint beste` DECIMAL(5,3),
	`CoD links 1` DECIMAL(4,2),
	`CoD links 2` DECIMAL(4,2),
	`CoD links beste` DECIMAL(4,2),
	`CoD rechts 1` DECIMAL(4,2),
	`CoD rechts 2` DECIMAL(4,2),
	`CoD rechts beste` DECIMAL(4,2),
	`Vertesprong 1` DECIMAL(4,2),
	`Vertesprong 2` DECIMAL(4,2),
	`Vertesprong beste` DECIMAL(4,2),
	FOREIGN KEY (allocatie_id) REFERENCES allocatie(id)
);

-- Create a new table called 's2g' in schema 'ztiggele'
CREATE TABLE IF NOT EXISTS ztiggele.s2g
(
    `allocatie_id` INT NOT NULL PRIMARY KEY,
	`Invuldatum` DATE,
    `Aantal seizoenen` NVARCHAR(20),
	`Voetbalachtergrond - amateurclub` BIT,
	`Voetbalachtergrond - voetbalschool vd club` BIT,
	`Voetbalachtergrond - zelfstandige voetbalschool` BIT,
	`Voetbalachtergrond - andere profclub` BIT,
	`Voetbalachtergrond - geen` BIT,
	`Voetbalachtergrond - anders` NVARCHAR(50),
	`Voetbalschool` BIT,
	`Reistijd school-club` DECIMAL(3,0),
	`Reistijd huis-club` DECIMAL(3,0),
	`Jeugdinternational` BIT,
	`Rechts- of linksbenig` NVARCHAR(1),
	`Keeper` BIT,
	`Veldpositie horizontaal` NVARCHAR(50),
	`Veldpositie verticaal` NVARCHAR(50),
	`Contract met zaakwaarnemer` BIT,
	`Contract met club` BIT,
	`Intro- of extraversie` DECIMAL(1,0),
	`Emotionele instabiliteit` DECIMAL(3,0),
	`Hoge eisen stelle` DECIMAL(3,0),
	`Voldoen aan hoge eisen` DECIMAL(3,0),
	`Positief - intern` DECIMAL(3,0),
	`Negatief - extern` DECIMAL(3,0),
	`Fixed mindset` DECIMAL(3,0),
	`Negatief - intern` DECIMAL(3,0),
	`Positief - extern` DECIMAL(3,0),
	`Eigen vaardigheden/prestaties` DECIMAL(3,0),
	`Concurrentie met anderen` DECIMAL(3,0),
	`Mening van anderen` DECIMAL(3,0),
	`Plan maken` DECIMAL(3,0),
	`Piekeren` DECIMAL(3,0),
	`Afleiding zoeken` DECIMAL(3,0),
	`Positief heroriënteren` DECIMAL(3,0),
	`Emotionele steun zoeken` DECIMAL(3,0),
	`Weerbaar zijn` DECIMAL(3,0),
	`In perspectief plaatsen` DECIMAL(3,0),
	`Liegen` DECIMAL(3,0),
	`Emoties uiten` DECIMAL(3,0),
	`Positief blijven` DECIMAL(3,0),
	`Fantaseren` DECIMAL(3,0),
	`Afwachten` DECIMAL(3,0),
	`Opgeven` DECIMAL(3,0),
	`Ontspanning zoeken` DECIMAL(3,0),
	`Discussiëren` DECIMAL(3,0),
	`Schuld afschuiven` DECIMAL(3,0),
	`Zelfkritiek` DECIMAL(3,0),
	`Hulp zoeken` DECIMAL(3,0),
	`Vergeven` DECIMAL(3,0),
	`Digitale afleiding` DECIMAL(3,0),
	`Actief aanpakken` DECIMAL(3,0),
	`Emoties onderdrukken` DECIMAL(3,0),
	`Positief herwaarderen` DECIMAL(3,0),
	`Accepteren` DECIMAL(3,0),
	`Keuzevrijheid tevredenheid` DECIMAL(3,0),
	`Verbondenheid frustratie` DECIMAL(3,0),
	`Keuzevrijheid frustratie` DECIMAL(3,0),
	`Bekwaamheid frustratie` DECIMAL(3,0),
	`Bekwaamheid tevredenheid` DECIMAL(3,0),
	`Verbondenheid tevredenheid` DECIMAL(3,0),
	`Tevredenheid voelen` DECIMAL(3,0),
	`Ontwikkeling voelen` DECIMAL(3,0),
	`Kunnen voetballen (twee weken)` DECIMAL(3,0),
	`Plezier voelen` DECIMAL(3,0),
	`Vrij in hoofd voelen` DECIMAL(3,0),
	`Faalangst - Bezwijken onder druk` DECIMAL(3,0),
	`Faalangst - Lichamelijk effect` DECIMAL(3,0),
	`Faalangst - Situationeel effect` DECIMAL(3,0),
	`Faalangst - Cognitief-emotionele verklaring` DECIMAL(3,0),
	`Faalangst - Risico vermijden` DECIMAL(3,0),
	`Draagkracht` DECIMAL(3,0),
	`Draaglast` DECIMAL(3,0),
	`Gespannen voelen` DECIMAL(3,0),
	`Somber voelen` DECIMAL(3,0),
	`emoedstoestand i.r.t. voetballeven` DECIMAL(3,0),
	`Zorgen maken` DECIMAL(3,0),
	`Zorgen maken i.r.t. voetballeven` DECIMAL(3,0),
	`Stress in voetballeven` DECIMAL(3,0),
	`Hoop op doorstroming binnen club` DECIMAL(3,0),
	`Hoop om profvoetballer te worden` DECIMAL(3,0),
	`Interne mentale begeleider` BIT,
	`Interne mentale begeleidingsduur per maand` DECIMAL(3,0),
	`Tevredenheid over interne mentale begeleider` DECIMAL(3,0),
	`Externe mentale begeleider` BIT,
	`Weet over externe mentale begeleider` BIT,
	`Externe mentale begeleidingsduur per maand` DECIMAL(3,0),
	`Tevredenheid over externe mentale begeleider` DECIMAL(3,0),
	`Mentale vaardigheden` DECIMAL(3,0),
	`Toepassing mentale vaardigheden` DECIMAL(3,0),
	`Behulpzaamheid mentale vaardigheden` DECIMAL(3,0),
	`Blessurestatus` DECIMAL(3,0),
	`Blessureduur - verleden` DECIMAL(3,0),
	`Blessureduur - toekomst` DECIMAL(3,0),
	`Speelstatus wedstrijd 1` DECIMAL(3,0),
	`Zelfbeoordeling wedstrijd 1` DECIMAL(3,0),
	`Speelstatus wedstrijd 2` DECIMAL(3,0),
	`Zelfbeoordeling wedstrijd 2` DECIMAL(3,0),
	`Speelstatus wedstrijd 3` DECIMAL(3,0),
	`Zelfbeoordeling wedstrijd 3` DECIMAL(3,0),
	`Speeltijd` DECIMAL(3,0),
	`Volledig kunnen trainen (4 weken)` DECIMAL(3,0),
	`Zelfbeoordeling trainingsprestatie` DECIMAL(3,0),
	`Prestatieniveau` DECIMAL(3,0),
	`Negatief op fouten reageren` DECIMAL(3,0),
	`Algemeen coachgedrag` DECIMAL(3,0),
	`Fouten maken stimuleren` DECIMAL(3,0),
	`Eerlijk zijn` DECIMAL(3,0),
	`Prestaties waarderen` DECIMAL(3,0),
	`Discutabele kritiek geven` DECIMAL(3,0),
	`Voorwaardelijk straffen` DECIMAL(3,0),
	`Eigenwaarde aantasten` DECIMAL(3,0),
	`Ontwikkeluitleg geven` DECIMAL(3,0),
	`Aandacht geven` DECIMAL(3,0),
	`Voorwaardelijk belonen` DECIMAL(3,0),
	`Duidelijkheid over besluiten verschaffen` DECIMAL(3,0),
	`Authenciteit belemmeren` DECIMAL(3,0),
	`E-oriëntatie (Winklimaat)` DECIMAL(3,0),
	`Competentie-oriëntatie (Ontwikkelklimaat)` DECIMAL(3,0),
	`Hoge eisen stellen trainer` DECIMAL(3,0),
	`Voldoen aan hoge eisten trainer` DECIMAL(3,0),
	`Indruk van de trainer` DECIMAL(3,0),
	`Ethiek van de trainer` DECIMAL(3,0),
	`Positieve teamsfeer` DECIMAL(3,0),
	`Exclusie` DECIMAL(3,0),
	`Negatief samenspel` DECIMAL(3,0),
	`Negatieve teamsfeer` DECIMAL(3,0),
	`Inclusie` DECIMAL(3,0),
	`Demotiveren` DECIMAL(3,0),
	`Ecentrisch spel` DECIMAL(3,0),
	`Motiveren` DECIMAL(3,0),
	`Gepest worden` DECIMAL(3,0),
	`Pesten` DECIMAL(3,0),
	`Zien dat anderen gepest worden` DECIMAL(3,0),
	`Discriminatie` DECIMAL(2,0),
	`Discriminatie aspect - geen` BIT,
	`Discriminatie aspect - afkomst` BIT,
	`Discriminatie aspect - religie` BIT,
	`Discriminatie aspect - lengte` BIT,
	`Discriminatie aspect - lichaamsbouw` BIT,
	`Discriminatie aspect - uiterlijk` BIT,
	`Discriminatie aspect - uitstraling` BIT,
	`Discriminatie aspect - kledingstijl` BIT,
	`Discriminatie aspect - opleidingsniveau` BIT,
	`Discriminatie aspect - huidskleur` BIT,
	`Discriminatie aspect - ouders` BIT,
	`Discriminatie aspect - voetbalkwaliteit` BIT,
	`Discriminatie aspect - persoonlijkheid` BIT,
	`Discriminatie aspect - cultuur` BIT,
	`Discriminatie aspect - leeftijd` BIT,
	`Discriminatie aspect - sexuele voorkeur` BIT,
	`Discriminatie aspect - iets anders` NVARCHAR(50),
	`Ouderlijke situatie` BIT,
	`Woonsituatie - beide ouders` BIT,
	`Woonsituatie - moeder` BIT,
	`Woonsituatie - vader` BIT,
	`Woonsituatie - andere familieleden` BIT,
	`Woonsituatie - gastgezin` BIT,
	`Woonsituatie - op mijzelf` BIT,
	`Woonsituatie - vrienden` BIT,
	`Woonsituatie - teamgenoten` BIT,
	`Woonsituatie - liefdespartner` BIT,
	`Woonsituatie - anders` NVARCHAR(75),
	`Instrumentele ondersteuning` DECIMAL(3,0),
	`Emotionele-informatieve ondersteuning` DECIMAL(3,0),
	`Scope van de ondersteuning` DECIMAL(3,0),
	`Betrokkenheid vader/verzorger` DECIMAL(3,0),
	`Betrokkenheid moeder/verzorgster` DECIMAL(3,0),
	`Hoe eisen van ouder(s)` DECIMAL(3,0),
	`Voldoen aan hoge eisen van ouder(s)` DECIMAL(3,0),
	`Sociale stress` DECIMAL(3,0),
	`Stress in privé leven` DECIMAL(3,0),
	`Slaapprobleem` DECIMAL(3,0),
	`Energieprobleem` DECIMAL(3,0),
	`Slaaptekort` DECIMAL(3,0),
    `Postcodegebied` DECIMAL(4,0),
	`Nederlandse nationaliteit` BIT,
	`Andere nationaliteit/afkomst` BIT,
	`Soort nationaliteit/afkomst` NVARCHAR(50),
	`Huidige opleidingsniveau` NVARCHAR(50),
	`Hoogst afgeronde opleiding` NVARCHAR(50),
	`Combinatie school en voetbal` DECIMAL(3,0),
	`Terugkoppeling scoreresultaten` BIT, 
	FOREIGN KEY (allocatie_id) REFERENCES allocatie(id)
);

-- Create a new table called 'bf' in schema 'ztiggele'
CREATE TABLE IF NOT EXISTS ztiggele.bf
(
    `allocatie_id` INT NOT NULL PRIMARY KEY,
    `position-label` NVARCHAR(40),
    `footed-label` NVARCHAR(30),
	`Test Date` DATE,
	`Test Time` TIME(0),
    `Wm1` DECIMAL(2,0),
    `Wm2` DECIMAL(2,0),
    `Wm3` DECIMAL(2,0),
    `Wm4` DECIMAL(2,0),
    `Wm5` DECIMAL(2,0),
    `Wm6` DECIMAL(2,0),
    `Wm7` DECIMAL(2,0),
    `Wm8` DECIMAL(2,0),
    `WmMean` DECIMAL(11,9),
    `Anticipation Total time Game played` DECIMAL(11,9),
	`Anticipation Time until Challenge` DECIMAL(11,9),
	`Anticipation Time in Challenge` DECIMAL(11,9),
	`Anticipation Points per second` DECIMAL(11,9),
	`Anticipation Points total` INT,
	`Control Accuracy Repeat 2 trials` DECIMAL(11,9),
	`Control Accuracy Repeat 3 trials` DECIMAL(11,9),
	`Control Accuracy Repeat 4 trials` DECIMAL(11,9),
	`Control Accuracy Repeat 5 trials` DECIMAL(11,9),
	`Control Rt Repeat 2 trials` DECIMAL(11,9),
	`Control Rt Repeat 3 trials` DECIMAL(11,9),
	`Control Rt Repeat 4 trials` DECIMAL(11,9),
	`Control Rt Repeat 5 trials` DECIMAL(11,9),
	`Control Rt Repeat Correct 2 trials` DECIMAL(11,9),
	`Control Rt Repeat Correct 3 trials` DECIMAL(11,9),
	`Control Rt Repeat Correct 4 trials` DECIMAL(11,9),
	`Control Rt Repeat Correct 5 trials` DECIMAL(11,9),
	`Control Accuracy No switch` DECIMAL(11,9),
	`Control Accuracy Motor switch` DECIMAL(11,9),
	`Control Accuracy Catery switch` DECIMAL(11,9),
	`Control RTe No switch` DECIMAL(11,9),
	`Control RTe Motor switch` DECIMAL(11,9),
	`Control RTe Catery switch` DECIMAL(11,9),
	`Control RT Correct No switch` DECIMAL(11,9),
	`Control RT Correct Motor switch` DECIMAL(11,9),
	`Control RT Correct Catery switch` DECIMAL(11,9),
	`Control RT 1 Fastest` DECIMAL(11,9),
	`Control Control RT 1 Slowest` DECIMAL(11,9),
	`Control Rt Mean` DECIMAL(11,9),
	`Control Rt Median` DECIMAL(11,9),
	`Control Points total` INT,
    `Attention Accuracy No Cue` DECIMAL(11,9),
	`Attention Accuracy Central Cue` DECIMAL(11,9),
	`Attention Accuracy Spatial Cue` DECIMAL(11,9),
	`Attention Accuracy Wrong Spatial Cue` DECIMAL(11,9),
	`Attention Accuracy Congruent` DECIMAL(11,9),
	`Attention Accuracy In congruent` DECIMAL(11,9),
	`Attention Rt No Cue` DECIMAL(11,9),
	`Attention Rt Central Cue` DECIMAL(11,9),
	`Attention Rt Spatial Cue` DECIMAL(11,9),
	`Attention Rt Wrong Spatial Cue` DECIMAL(11,9),
	`Attention Rt Congruent` DECIMAL(11,9),
	`Attention Rt In congruent` DECIMAL(11,9),
	`Attention Rt 1 Fastest` DECIMAL(11,9),
	`Attention Control RT 1 Slowest` DECIMAL(11,9),
	`Attention Rt Mean` DECIMAL(11,9),
	`Attention Rt Median` DECIMAL(11,9),
	`Attention Points Total` INT,
    `Wm Overall` DECIMAL(3,0),
	`Wm Capacity` DECIMAL(3,0),
	`Wm Identity` DECIMAL(3,0),
	`Wm Reselience` DECIMAL(3,0),
	`Wm Filtering` DECIMAL(3,0),
	`Anticipation Overall` DECIMAL(3,0),
	`Anticipation Performance` DECIMAL(3,0),
	`Anticipation Resilience` DECIMAL(3,0),
	`Control Overall` DECIMAL(3,0),
	`Control Speed` DECIMAL(3,0),
	`Control Automatic` DECIMAL(3,0),
	`Control Motor Inhibition` DECIMAL(3,0),
	`Control Mental Flexibilty` DECIMAL(3,0),
	`Attention Overall` DECIMAL(3,0),
	`Attention Speed` DECIMAL(3,0),
	`Attention Performance` DECIMAL(3,0),
	`Attention Concentration` DECIMAL(3,0),
	`Attention Move` DECIMAL(3,0),
	`Attention Disengage` DECIMAL(3,0),
	`Attention Guide` DECIMAL(3,0),
	`Data Quality Game1` BIT,
	`Data Quality Game2` BIT,
	`Data Quality Game3` BIT,
	`Data Quality Game4` BIT,
	`Topvoetbalmodel` DECIMAL(3,0),
	FOREIGN KEY (allocatie_id) REFERENCES allocatie(id)
);