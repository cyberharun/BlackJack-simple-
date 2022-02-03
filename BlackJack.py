#BlackJack
#1 do 7 osoba igraju protiv djelioca

import modul,modulefromPlayingCards

class BJ_Card(modul.Card):
    """Karta u igri BlackJack"""
    ACE_VALUE=1

    @property
    def value(self):
        if self.is_face_up:
            v=BJ_Card.RANKS.index(self.rank)+1 #dodaje se 1 jer index iz liste za broj npr 6 je 5
            if v>10:
                v=10
        else:
            v=None
        return v

class BJ_Deck(modul.Deck):
    """Predstavlja spil karata u igri BlackJack"""
    def populate(self):
        for suit in BJ_Card.SUITS:
            for rank in BJ_Card.RANKS:
                self.cards.append(BJ_Card(rank,suit))
            #redefinisana metoda populate() da se nov objekat BJ_Deck inicijalizuje objektima tipa BJ_Card

class BJ_Hand(modul.Hand):
    """Predstavlja ruku u igri BlackJack"""
    def __init__(self,name):
        super(BJ_Hand,self).__init__()
        self.name=name

    def __str__(self):
        rep=self.name+":\t"+super(BJ_Hand,self).__str__()
        if self.total:
            rep+="("+str(self.total)+")"

        return rep

    @property
    def total(self):
        #ako jedna karta ima vrijednost None, cijela ruka je None
        for card in self.cards:
            if not card.value:
                return None

        #sabiranje  vrijednosti karata; svaki kec vrijedi 1
        t=0
        for card in self.cards:
            t+=card.value

        #odredjivanje da li ruka sadrzi keca
        contains_ace=False
        for card in self.cards:
            if card.value==BJ_Card.ACE_VALUE:
                contains_ace=True

        #ako ruka sadrzi keca i zbir je dovoljno nizak,
        #kec se broji kao 11
        if contains_ace and t<=11:
            #dodajemo 10 jer smo vec dodali jedan za keca
            t+=10

        return t

    def is_busted(self):
        return self.total>21


class BJ_Player(BJ_Hand):
    """Predstavlja igraca u igri BlackJack"""
    def is_hitting(self):
        response=modulefromPlayingCards.ask_yes_no("\n"+self.name+" , do you want a hit (y/n)?:")
        return response=="y"

    def bust(self):
        print(self.name, " busts.")
        self.lose()

    def lose(self):
        print(self.name, " loses.")

    def win(self):
        print(self.name, " wins.")

    def push(self):
        print(self.name, " pushes.")


class BJ_Dealer(BJ_Hand):
    """Predstavlja djelioca  u igri BlackJack"""
    def is_hitting(self):
        return self.total<17

    def bust(self):
        print(self.name, " busts.")

    def flip_first_card(self):
        first_card=self.cards[0]
        first_card.flip()


class BJ_Game(object):
    """Predstavlja partiju igre BlackJack"""
    def __init__(self,names):
        self.players=[]
        for name in names:
            player=BJ_Player(name)
            self.players.append(player)

        self.dealer=BJ_Dealer("Dealer")

        self.deck=BJ_Deck()
        self.deck.populate()
        self.deck.shuffle()


    @property
    def still_playing(self):
        sp=[]
        for player in self.players:
            if not player.is_busted():
                sp.append(player)

        return sp


    def __addiotional_cards(self,player):
        while not player.is_busted() and player.is_hitting():
            self.deck.deal([player])
            print(player)
            if player.is_busted():
                player.bust()


    def play(self):
        #podijelite svakome po dve pocetne karte
        self.deck.deal(self.players+[self.dealer],per_hand=2)
        self.dealer.flip_first_card()      #sakriti prvu djeliocevu kartu
        for player in self.players:
            print(player)
        print(self.dealer)

        #podijelite dodatne karte igracima
        for player in self.players:
            self.__addiotional_cards(player)

        self.dealer.flip_first_card()    #Pokazati prvu djeliocevu kartu

        if not self.still_playing:
            #posto su svi igraci tropa, prikazati sadrzaj djelioceve ruke
            print(self.dealer)
        else:
            #dijeli dodatne karte djeliocu
            print(self.dealer)
            self.__addiotional_cards(self.dealer)

        if self.dealer.is_busted():
            #povjednici su svi koji su i dalje u igri
            for player in self.still_playing:
                player.win()
        else:
            #poredjenje zbira svakog igraca sa djeliocevim zbirom
            for player in self.still_playing:
                if player.total>self.dealer.total:
                    player.win()
                elif player.total==self.dealer.total:
                    player.push()
                else:
                    player.lose()

        #uklonuti karte svih igraca
        for player in self.players:
            player.clear()
        self.dealer.clear()

def main():
    print("\tWelcome to BlackJack !\n")

    names=[]
    number=modulefromPlayingCards.ask_number("How many players ? (1-7):", low=1,high=8)

    for i in range(number):
        name=input("Enter player name: ")
        names.append(name)

    print()

    game=BJ_Game(names)

    again=None
    while again!="n":
        game.play()
        again=modulefromPlayingCards.ask_yes_no("\nDo you want to play again ? :")

main()
input("\n\nPress the enter key to exit!!!")
