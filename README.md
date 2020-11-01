# Redis datu bāzes tests

## Datu bāzes piemērs, kurā attēlota interneta blogu lapa.

## Dati un to respektīvie redis objekti:
>_**Person**_ - hash, kas satur pamatinformācija par cilvēku

>_**Author**_ - hash, kas papildina informāciju par cilvēku. Lietotāja objekts lapā

>_**Topic**_ - set, kas satur nesakārtotu sarakstu ar iespējamām rakstu tēmām

>_**Post**_ - hash, kas satur visu informāciju par saglabātajiem rakstiem datu bāzē.

>_**AUTHOR_IDS**_ - Set

>_**POST_IDS**_ Set
