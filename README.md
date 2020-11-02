# Redis datu bāzes tests

Datu bāzes piemērs, kurā attēlota interneta blogu lapa.

## Dati un to respektīvie redis objekti:
>_**Person**_ - hash. Pamatinformācija par cilvēku:

1. name
2. surname
3. age
4. phone

>_**Author**_ - hash. Papildina Person. Autora informācija:

1. author_ID
2. person_ID
3. username
4. password
5. total_posts

>_**AUTHOR_IDS**_ - set. Kopa, kas satur eksistejoso autoru indeksus

>_**Topic**_ - set. Kopa, kas satur nesakārtotu sarakstu ar iespējamām rakstu tēmām

>_**Post**_ - hash. Satur visu informāciju par saglabātajiem rakstiem:

1. post_ID
2. author_ID
3. title
4. text
5. topic
6. date
7. timestamp

>_**POST_IDS**_ - set. Kopa, kas satur eksistejoso postu indeksus
