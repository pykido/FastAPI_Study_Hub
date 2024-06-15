import databases
import sqlalchemy

# SQLAlchemy specific code, as with any other app
DATABASE_URL = "sqlite:///./sqlite_crud.db"	# database의 url

# 만약 PostgreSQL같은 다른 SQL을 사용한다면 다른 DATABASE_URL을 사용해야 함!
# DATABASE_URL = "postgresql://user:password@postgresserver/db"

# DATABASE_URL에 database 객체를 생성
database = databases.Database(DATABASE_URL)

# SQLAlchemy로부터 메타데이터 생성
metadata = sqlalchemy.MetaData()

# notes 테이블 생성
notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)

# SQLAlchemy 엔진 생성
## SQLite를 DB로 사용하자
## SQLite는 기본적으로 멀티 스레드 환경에서 database 접근을 허용하지 않기에 멀티 스레드 접근을 허용하도록 설정
engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
## metadata 객체가 포함된 모든 테이블들을 실제 DB에 생성. 즉, notes 테이블을 DB에 생성
metadata.create_all(engine)