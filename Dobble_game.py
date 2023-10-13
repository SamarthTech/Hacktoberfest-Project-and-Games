from random import shuffle

#List of symbols used in the game Dobble (Spot It! in the US)
symbols = ["Anchor","Apple","Bomb","Cactus","Candle","Carrot",
  "Cheese","Chess knight","Clock","Clown","Diasy flower","Dinosaur",
  "Dolphin","Dragon","Exclamation mark","Eye","Fire","Four leaf clover",
  "Ghost","Green splats","Hammer","Heart","Ice cube","Igloo","Key",
  "Ladybird","Light bulb","Lightning bolt","Lock","Maple leaf","Milk bottle",
  "Moon","No Entry sign","Orange scarecrow man","Pencil","Purple bird",
  "Purple cat","Purple dobble sign","Question Mark","Red lips","Scissors",
  "Skull and crossbones","Snowflake","Snowman","Spider","Spider’s web",
  "Sun","Sunglasses","Target","Taxi","Tortoise","Treble clef","Tree",
  "Water drop","Dog","Yin and Yang","Zebra"]

#The number of symbols on a card has to be a prime number + 1
numberOfSymbolsOnCard = 8   #(7 + 1)
shuffleSymbolsOnCard = False

cards = []

#Work out the prime number
n = numberOfSymbolsOnCard - 1

#Total number of cards that can be generated following the Dobble rules
numberOfCards = n**2 + n + 1  #e.g. 7^2 + 7 + 1 = 57


#Add first set of n+1 cards (e.g. 8 cards)
for i in range(n+1):  
  #Add new card with first symbol
  cards.append([1])
  #Add n+1 symbols on the card (e.g. 8 symbols)
  for j in range(n):
    cards[i].append((j+1)+(i*n)+1)

#Add n sets of n cards 
for i in range(0,n):
  for j in range(0,n):
    #Append a new card with 1 symbol
    cards.append([i+2])
     #Add n symbols on the card (e.g. 7 symbols)
    for k in range(0,n):
      val  = (n+1 + n*k + (i*k+j)%n)+1
      cards[len(cards)-1].append(val)

#Shuffle symbols on each card
if shuffleSymbolsOnCard :
  for card in cards:
    shuffle(card)
      
#Output all cards  
i = 0
for card in cards:
  i+=1
  line = str(i) + " - ["
  for number in card:
    line = line + symbols[number-1] + ", "
  line = line[:-2] + "]"  
  print(line)