from elixir import *

metadata.bind = "sqlite:///movies.sqlite"
metadata.bind.echo = True

class Movie(Entity):
    title = Field(Unicode(30))
    year = Field(Integer)
    description = Field(UnicodeText)
    
    def __repr__(self):
        return '<Movie "%s" (%d)>' % (self.title, self.year)

def test():
    setup_all()
    create_all()
    m1 = Movie( title = 'Film1', year = 1990 )
    m2 = Movie( title = 'Film2', year = 1991 )
    m3 = Movie( title = 'Film3', year = 1992 )
    m4 = Movie( title = 'Film4', year = 1993 )
    session.commit()
    del m1
    del m2
    del m3
    del m4
    for m in Movie.query.all():
        print m
        

if __name__ == '__main__':
    test()
