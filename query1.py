from data.db_session import create_session, global_init
from data.users import User

db = input()
data = global_init(db)
session = create_session()
users = session.query(User).filter(User.address == "module_1",
                                   User.speciality.notilike('%engineer%'),
                                   User.position.notilike('%engineer%')).all()
for user_ in users:
    print(user_.id)




