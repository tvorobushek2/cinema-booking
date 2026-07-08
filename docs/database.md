\# 🗄 Схема базы данных Cinema Booking



\## 1. halls (Кинотеатральные залы)

| Поле   | Тип         | Ограничения      | Описание          |

|--------|-------------|------------------|-------------------|

| id     | SERIAL      | PRIMARY KEY      | Уникальный ID     |

| number | INTEGER     | NOT NULL, UNIQUE | Номер зала (1,2,3)|

| name   | VARCHAR(50) | NOT NULL         | Название ("IMAX") |



\## 2. rows (Ряды)

| Поле    | Тип     | Ограничения                | Описание      |

|---------|---------|----------------------------|---------------|

| id      | SERIAL  | PRIMARY KEY                | Уникальный ID |

| hall\_id | INTEGER | FK -> halls(id), NOT NULL  | Привязка к залу|

| number  | INTEGER | NOT NULL                   | Номер ряда    |

| \*UNIQUE\*|         | (hall\_id, number)          |               |



\## 3. seats (Места)

| Поле    | Тип         | Ограничения                | Описание               |

|---------|-------------|----------------------------|------------------------|

| id      | SERIAL      | PRIMARY KEY                | Уникальный ID          |

| row\_id  | INTEGER     | FK -> rows(id), NOT NULL   | Привязка к ряду        |

| number  | INTEGER     | NOT NULL                   | Номер места            |

| type    | VARCHAR(10) | NOT NULL, DEFAULT 'standard'| 'standard' или 'vip'  |

| price   | DECIMAL(10,2)| NOT NULL                  | Цена билета (300.00)   |

| \*UNIQUE\*|             | (row\_id, number)           |                        |



\## 4. sessions (Сеансы)

| Поле       | Тип         | Ограничения                | Описание              |

|------------|-------------|----------------------------|-----------------------|

| id         | SERIAL      | PRIMARY KEY                | Уникальный ID         |

| hall\_id    | INTEGER     | FK -> halls(id), NOT NULL  | В каком зале идет     |

| title      | VARCHAR(200)| NOT NULL                   | Название фильма       |

| started\_at | TIMESTAMP   | NOT NULL                   | Время начала          |

| duration   | INTEGER     | NOT NULL                   | Длительность в минутах|



\## 5. bookings (Брони) - Зона Кирилла

| Поле       | Тип         | Ограничения                | Описание                      |

|------------|-------------|----------------------------|-------------------------------|

| id         | SERIAL      | PRIMARY KEY                | Уникальный ID                 |

| user\_id    | INTEGER     | NOT NULL                   | ID пользователя (заглушка)    |

| session\_id | INTEGER     | FK -> sessions(id), NOT NULL| К какому сеансу             |

| seat\_id    | INTEGER     | FK -> seats(id), NOT NULL  | Какое место                   |

| status     | VARCHAR(10) | NOT NULL                   | 'awaiting', 'paid', 'expired' |

| created\_at | TIMESTAMP   | DEFAULT NOW()              | Время создания брони          |

| expires\_at | TIMESTAMP   | NOT NULL                   | created\_at + 15 минут         |

