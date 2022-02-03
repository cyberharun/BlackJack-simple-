#Games
#Prikazuje izradu modula

class Player(object):
    """Ucesnik u igri"""
    def __init__(self,name,score=0):
        self.name=name
        self.score=score

    def __str__(self):
        rep=self.name+":\t"+str(self.score)
        return rep

def ask_yes_no(question):
    """Prikazuje pitanje na koje odgovor moze biti yes ili no"""
    response=None
    while response not in("y","n"):
        response=input(question).lower()
    return response

def ask_number(question,low,high):
    """Zahtjeva od korisnika da upise broj u datom opsegu"""
    response=None
    while response not in range(low,high):
        response=int(input(question))
    return response

if __name__=="__main__":
    print("You ran this module directly(and did not 'import' it).")
    input("\n\nPress enter to exit.")