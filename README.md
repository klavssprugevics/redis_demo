# Redis datu bāzes tests

Datu bāzes piemērs, kurā attēlota interneta blogu lapa.

## Dati un to respektīvie redis objekti:
>_**Person**_ - hash. Pamatinformācija par cilvēku:

name
surname
age
phone

>_**Author**_ - hash. Papildina Person. Autora informācija:

author_ID
person_ID
username
password
total_posts

>_**AUTHOR_IDS**_ - set. Kopa, kas satur eksistejoso autoru indeksus

>_**Topic**_ - set. Kopa, kas satur nesakārtotu sarakstu ar iespējamām rakstu tēmām

>_**Post**_ - hash. Satur visu informāciju par saglabātajiem rakstiem:

post_ID
author_ID
title
text
topic
date
timestamp

>_**POST_IDS**_ - set. Kopa, kas satur eksistejoso postu indeksus
