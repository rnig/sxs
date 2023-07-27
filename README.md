# xs
special xml services



## xx

De xx  module is enkel bedoeld om "iets" te weten te komen over "sommige interessante tags" 
in een mogelijk (heel) groot XML bestand.

Voorbeeld:

'''
(sxs) d:\sxs>py src\xx.py
Welke file wil je verwerken?dat\in\sample.xml
In welke file wil je extracts dumpen?dat\out\sample-xx.txt
Als je alles wil verwerken druk [a]
of als enkel een staal wil nemen druk [s].s
Input bestand dat\in\sample.xml werd gesloten.
After 0.011341333389282227 seconds we counted 140 characters and 0 interesting tag occurrences.
0
{'RRNIdentification': [], 'KBONumberIdentification': []}
Do you want to collect interesting tags?n
[]
'''



## xf

De module  xf is bedoeld om  een lange xml lijn  te herformateren in
ietwat leesbare door regeleinden afgebakende tekst.

Voorbeeld:

'''
(sxs) d:\sxs>py src\xf.py
Welke file wil je verwerken?dat\out\sample-cy.txt
Naar welke file wil je schrijven?dat\out\sample-cy.xml
xml_line_counter=0, output_line='<?xml version="1.0" encoding="UTF-8"?>\n', nested_level=0
xml_line_counter=1, output_line='<Extract xmlns="http://www.nbb.be/cba/2021-06/extract">\n', nested_level=0
xml_line_counter=2, inline='____<Header>\n', nested_level=1
xml_line_counter=3, inline='________<DeclarerId>\n', nested_level=2
xml_line_counter=4, inline='____________<DeclarerKBONumber>\n', nested_level=3
xml_line_counter=5, output_line='0403288089</DeclarerKBONumber>', , end_data_index=10, nested_level=3
xml_line_counter=5, inline='________________0403288089\n', nested_level=3
xml_line_counter=6, inline='____________</DeclarerKBONumber>\n', nested_level=3
xml_line_counter=7, output_line='</DeclarerId>', , end_data_index=0, nested_level=2
xml_line_counter=7, inline='________</DeclarerId>\n', nested_level=2
xml_line_counter=8, inline='________<ExtractDate>\n', nested_level=2
...
'''

en het output bestand start dan als volgt:

'''
<?xml version="1.0" encoding="UTF-8"?>
<Extract xmlns="http://www.nbb.be/cba/2021-06/extract">
____<Header>
________<DeclarerId>
____________<DeclarerKBONumber>
________________0403288089
____________</DeclarerKBONumber>
________</DeclarerId>
________<ExtractDate>
____________2023-06-05
________</ExtractDate>
________<FileNumber>
____________1
________</FileNumber>
________<FileReference>
____________0403288089-20230605-20230605-00001523-NoPeriod-00000001.xml
________</FileReference>
____</Header>
...
'''



## ef

De module  ef is bedoeld om  het voorkomen in aantal  van een selectie
van tags op te sommen in aparte tekst bestanden per tag.

Voorbeeld, gegeven dit stuk xml:

'''
<?xml version="1.0" encoding="UTF-8"?><Extract xmlns="http://www.nbb.be/cba/2021-06/extract"><Header><DeclarerId><DeclarerKBONumber>0403288089</DeclarerKBONumber></DeclarerId><ExtractDate>2023-06-05</ExtractDate><FileNumber>1</FileNumber><FileReference>0403288089-20230605-20230605-00001523-NoPeriod-00000001.xml</FileReference></Header><Customer CustomerSequenceNumber="1"><CustomerIdentification><NaturalPersonId><RRNIdentification>36013029454</RRNIdentification></NaturalPersonId></CustomerIdentification><CustomerRelations><Contracts><Contract><ContractTypeName>LifeInsurance</ContractTypeName><CustomerStartDate>2021-03-25</CustomerStartDate><CustomerEndDate>9999-12-31</CustomerEndDate><Amounts><Amount ValueDate="2021-12-31">99845.13</Amount><Amount ValueDate="2022-12-31">101026.51</Amount></Amounts></Contract></Contracts></CustomerRelations></Customer><Customer CustomerSequenceNumber="2"><CustomerIdentification><EntityIdentification><KBONumberIdentification>0871140370</KBONumberIdentification></EntityIdentification></CustomerIdentification><CustomerRelations><Contracts><Contract><ContractTypeName>LifeInsurance</ContractTypeName><CustomerStartDate>2020-01-01</CustomerStartDate><CustomerEndDate>9999-12-31</CustomerEndDate><Amounts><Amount ValueDate="2020-12-31">43179.21</Amount><Amount ValueDate="2021-12-31">49791.44</Amount></Amounts></Contract></Contracts></CustomerRelations></Customer><Customer CustomerSequenceNumber="49"><CustomerIdentification><EntityIdentification><KBONumberIdentification>0446938683</KBONumberIdentification></EntityIdentification></CustomerIdentification><CustomerRelations><Contracts><Contract><ContractTypeName>MortgageLoan</ContractTypeName><CustomerStartDate>2022-07-08</CustomerStartDate><CustomerEndDate>9999-12-31</CustomerEndDate></Contract></Contracts></CustomerRelations></Customer></Extract>
'''

Deze verwerking:

'''
(sxs) d:\sxs>py src\ef.py
Welke file wil je verwerken?dat\out\sample-cy.txt
Naar welke file wil je schrijven?dat\out\sample-cy-ef.txt
After 0.0299985408782959 seconds we counted 1848 characters and reformatted 107 lines.
To which folder do you want to write the fields focused upon?dat\out
Field '<RRNIdentification>' has 1 relations.
Field '<KBONumberIdentification>' has 2 relations.
Field '<ContractTypeName>' has 3 relations.
3.
'''

Krijg je dit als resultaat:

'''
  d:/sxs/dat/out:
  total used in directory 26 available 18.7 GiB
  -rw-rw-rw-  1 erwin erwin   13 07-26 05:33 RRNIdentification.txt
  -rw-rw-rw-  1 erwin erwin  397 07-26 05:33 records.txt
  -rw-rw-rw-  1 erwin erwin   24 07-26 05:33 KBONumberIdentification.txt
  -rw-rw-rw-  1 erwin erwin   29 07-26 05:33 ContractTypeName.txt
...
'''

Waarbij RRNIdentification.txt dit bevat:

'''
36013029454
'''

En KBONumberIdentification.txt:

'''
0446938683
0871140370
'''

En ContractTypeName.txt:

'''
LifeInsurance
MortgageLoan
'''

Tenslotte records.txt:

'''
36013029454|LifeInsurance
0871140370|LifeInsurance
0446938683|MortgageLoan
'''



## tail

De module tail is een imitatie van de unix tail.

Bijv:

'''
(sxs) d:\sxs>py src\tail.py 5 dat\out\sample-cy.txt dat\out\sample-cy-tail5.txt
After 0.025002717971801758  seconds we  counted 1847  characters and
the last 5 were written to dat\out\sample-cy-tail5.txt.

(sxs) d:\sxs>py src\tail.py 15 dat\out\sample-cy.txt dat\out\sample-cy-tail15.txt
After 0.02499675750732422 seconds we counted 1847 characters and the
last 15 were written to dat\out\sample-cy-tail15.txt.
'''



## head

De module head is een imitatie van de unix head.

Bijv:

'''
sxs) d:\sxs>py src\head.py 5 dat\out\sample-cy.xml
<?xml

(sxs) d:\sxs>py src\head.py 15 dat\out\sample-cy.xml
<?xml version="

(sxs) d:\sxs>py src\head.py 150 dat\out\sample-cy.xml
<?xml version="1.0" encoding="UTF-8"?>
<Extract xmlns="http://www.nbb.be/cba/2021-06/extract">
____<Header>
________<DeclarerId>
____________<Declarer
...
'''



## rx : render xml from (template, data)

Gegeven een XML-context onder de vorm  van een Jinja2 template, kan je
invulwaarden  injecteren  en  uit   het  samengestelde  resultaat  een
afgevulde XML file afleveren.
(sxs) d:\sxs>py src\rx.py
Waar staat de data?ttt\declaration_data.csv
return_path: cfg\declaration_header.xml
return_path: cfg\declaration_rrn-header.xml
return_path: cfg\declaration_close.xml
return_path: cfg\declaration_rrn-footer.xml
return_path: cfg\declaration_footer.xml
Naar welk bestand mag het gegenereerde resultaat worden geschreven?tmp\declaration-coup-de-poing.xml

Een mogelijkse snipper template kan zijn:

'''
<?xml version="1.0" encoding="UTF-8"?>
<DeclarationRequest xmlns="http://www.nbb.be/cba/2019-04/declaration">
	<Header>
		<DeclarerId>
			<DeclarerKBONumber>{{ DeclarerKBONumber }}</DeclarerKBONumber>
		</DeclarerId>
		<ReportingDate>{{ ReportingDate }}</ReportingDate>
		<FileNumber>{{ FileNumber }}</FileNumber>
		<FileReference>{{ FileReference }}</FileReference>
	</Header>
...
'''

De invulwaarden zijn dan bijv:

'''
tag                        ; value
DeclarerKBONumber          ; 0403288089
ReportingDate              ; 2023-08-04
FileNumber                 ; 1
FileReference              ; test-1.xml
CustomerSequenceNumber     ; auto
CustomerBankIdentification ; wasdeesna
RRNIdentification          ; official rrn
RelationSequenceNumber     ; wasdana
ContractTypeName           ; LeasingContract
CustomerEndDate            ; 2023-06-06
'''


## cx :



## 