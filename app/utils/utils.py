from typing_extensions import Annotated
from sqlalchemy.orm import mapped_column
from sqlalchemy import Text, BIGINT, String, Numeric, Date
from datetime import date

int_big = Annotated[int, mapped_column(BIGINT)]

str_10 = Annotated[str, mapped_column(String(10))]
str_30 = Annotated[str, mapped_column(String(30))]
str_50 = Annotated[str, mapped_column(String(50))]
str_100 = Annotated[str, mapped_column(String(100))]
str_255 = Annotated[str, mapped_column(String(255))]

text = Annotated[str, mapped_column(Text)]

numeric_10_2 = Annotated[float, mapped_column(Numeric(10,2))]

date_ = Annotated[date, mapped_column(Date)]

