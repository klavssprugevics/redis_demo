# Redis datu bāzes tests

## Datu bāzes piemērs, kurā attēlota interneta blogu lapa.

## Dati un to respektīvie redis objekti:
>Person - hash, kas satur pamatinformācija par cilvēku
>Author - hash, kas papildina informāciju par cilvēku. Lietotāja objekts lapā
>Topic - set, kas satur nesakārtotu sarakstu ar iespējamām rakstu tēmām
>Post - hash, kas satur visu informāciju par saglabātajiem rakstiem datu bāzē.
