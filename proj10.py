#project 10 is to create a program that emulates a game of solitare. We are given a random deck of cards
#and have to create functions that validate whether a move can be made and then move if move is valid.
#the main function gives the user options for moves or to display, restart, quit and undo



#DO NOT DELETE THESE LINES
import cards, random
random.seed(100) #random number generator will always generate 
                 #the same 'random' number (needed to replicate tests)

MENU = '''     
Input options:
    MTT s d: Move card from Tableau pile s to Tableau pile d.
    MTF s d: Move card from Tableau pile s to Foundation d.
    MFT s d: Move card from Foundation s to Tableau pile d.
    U: Undo the last valid move.
    R: Restart the game (after shuffling)
    H: Display this menu of choices
    Q: Quit the game       
'''
                
def initialize():
    foundation = [[],[],[],[]]#create foundation
    tableau = [[],[],[],[],[],[],[],[]] #create tableau
    stock = cards.Deck() #create deck
    stock.shuffle() #shuffle deck
    tab0 = tableau[0] #initialize tableaus as lists
    tab1 = tableau[1]
    tab2 = tableau[2]
    tab3 = tableau[3]
    tab4 = tableau[4]
    tab5 = tableau[5]
    tab6 = tableau[6]
    tab7 = tableau[7]
    for i in range(7): #deal cards to lists with the specified number of cards (using range for amount)
        tab0.append(stock.deal())
    for i in range(6):
        tab1.append(stock.deal())
    for i in range(7):
        tab2.append(stock.deal())
    for i in range(6):
        tab3.append(stock.deal())
    for i in range(7):
        tab4.append(stock.deal())
    for i in range(6):
        tab5.append(stock.deal())
    for i in range(7):
        tab6.append(stock.deal())
    for i in range(6):
        tab7.append(stock.deal())
        
        
    return(tableau,foundation) #return bothh tableau and foundation
    
    
    

def display(tableau, foundation):
    '''Each row of the display will have
       tableau - foundation - tableau
       Initially, even indexed tableaus have 7 cards; odds 6.
       The challenge is the get the left vertical bars
       to line up no matter the lengths of the even indexed piles.'''
    
    # To get the left bars to line up we need to
    # find the length of the longest even-indexed tableau list,
    #     i.e. those in the first, leftmost column
    # The "4*" accounts for a card plus 1 space having a width of 4
    max_tab = 4*max([len(lst) for i,lst in enumerate(tableau) if i%2==0])
    # display header
    print("{1:>{0}s} | {2} | {3}".format(max_tab+2,"Tableau","Foundation","Tableau"))
    # display tableau | foundation | tableau
    for i in range(4):
        left_lst = tableau[2*i] # even index
        right_lst = tableau[2*i + 1] # odd index
        # first build a string so we can format the even-index pile
        s = ''
        s += "{}: ".format(2*i)  # index
        for c in left_lst:  # cards in even-indexed pile
            s += "{} ".format(c)
        # display the even-indexed cards; the "+3" is for the index, colon and space
        # the "{1:<{0}s}" format allows us to incorporate the max_tab as the width
        # so the first vertical-bar lines up
        print("{1:<{0}s}".format(max_tab+3,s),end='')
        # next print the foundation
        # get foundation value or space if empty
        found = str(foundation[i][-1]) if foundation[i] else ' '
        print("|{:^12s}|".format(found),end="")
        # print the odd-indexed pile
        print("{:d}: ".format(2*i+1),end="") 
        for c in right_lst:
            print("{} ".format(c),end="") 
        print()  # end of line
    print()
    print("-"*80)
          
def valid_tableau_to_tableau(tableau,s,d):
    s = int(s) #name source as given input
    d = int(d) #name destination as given input
    if s<0 or s>7: #if source number is not real list return false
        return  False
    if s>0 and s<7: #if source number is real list
        if tableau[s] != []: #if source tableau is not empty
            if tableau[d] != []:  #if destination tableau is not empty
                if tableau[d][-1].rank() - tableau[s][-1].rank() != 1: #if card is not one less than des card
                    return False
                if tableau[d][-1].rank() - tableau[s][-1].rank() == 1: #if card is one less than des card
                    return True
            if tableau[d] == []: #if destination any card can be added
                return True
        if tableau[s] == []: # if there is no source card to add
            return False
    
    else:
        return True
        
    
    
    
def move_tableau_to_tableau(tableau,s,d):
    result = valid_tableau_to_tableau(tableau,s,d)
    if result== True: #if valid function returns true
        card = tableau[s].pop() #pop card from source list
        tableau[d].append(card) #append valid move to destination list
    return(result)

def valid_foundation_to_tableau(tableau,foundation,s,d):
    if foundation[s] == []: #if there is no card return false
        return False
    if foundation[s] != []: #if there is a source card
        if tableau[d] == []: #if destination tab is empty any card can be added
            return True
        if tableau[d][-1].rank() - foundation[s][-1].rank() != 1:#if card is not one less than des card
            return False
        if tableau[d][-1].rank() - foundation[s][-1].rank() == 1:#if card is one less than des card
            return True
        
    
    
    

def move_foundation_to_tableau(tableau,foundation,s,d):
    result = valid_foundation_to_tableau(tableau,foundation,s,d)
    if result== True:#if valid function returns true
        card = foundation[s].pop()#pop card from source list
        tableau[d].append(card)#append valid move to destination list
    return(result)
    

def valid_tableau_to_foundation(tableau,foundation,s,d):
    if tableau[s] == []:#if there is no card return false
        return False
    if tableau[s] != []:#if there is a source card
        if foundation[d] == []: #this is so that only aces may be applied to empty foundations
            if tableau[s][-1].rank() == 1:
                return True
            if tableau[s][-1].rank() != 1:
                return False
        if tableau[s][-1].suit() != foundation[d][-1].suit(): #if suits are not same they cannot be added
            return False
        if tableau[s][-1].suit() == foundation[d][-1].suit(): #if suits are the same
                if foundation[d][-1].rank() - tableau[s][-1].rank() == -1: #only cards one more than card can be added
                    return True
                if foundation[d][-1].rank() - tableau[s][-1].rank() != -1:
                    return False
            
    
def move_tableau_to_foundation(tableau, foundation, s,d):
    result = valid_tableau_to_foundation(tableau,foundation,s,d)
    if result== True:#if valid function returns true
        card = tableau[s].pop()#pop card from source list
        foundation[d].append(card)#append valid move to destination list
    return(result)

def check_for_win(foundation):
    total = 0 #initalize total value
    for value in foundation:
        if value == []: #if foundation is empty skip that list
            continue
        total += value[-1].rank() #add together top foundation card ranks
    if total ==52: #if all are kings they add to 52 and the game has been won
        return True
    if total != 52:
        return False
        

def get_option():
    option_list = [] #empty options list so that return will be a list
    option = input("\nInput an option (MTT,MTF,MFT,U,R,H,Q): ").lower() #prompt for option
    done = False #set up  while loop
    while done != True:
        if option == 'r': #if restart is chosen append R to list return list and stop while  loop
            option_list.append('R')
            done = True
            return option_list
        if option == 'u':#if undo is chosen append U to list return list and stop while  loop
            option_list.append('U')
            done = True
            return option_list
        if option == 'h':#if display is chosen append H to list return list and stop while  loop
            option_list.append('H')
            done = True
            return option_list
        if option == 'q':#if quit is chosen append Q to list return list and stop while  loop
            option_list.append('Q')
            done = True
            print("Thank you for playing.") #print end statement
        if option not in ('r','u','h','q'): #if option is to make a move
            if option[:3] == 'mtt':
                if int(option[-3]) <0 or int(option[-3]) >7: #if source number is in number of source lists
                    print("Error in Source.") #error statement
                    option = input("\nInput an option (MTT,MTF,MFT,U,R,H,Q): ").lower()#reprompt for option
                    continue
                if int(option[-1]) <0 or int(option[-1]) >7:#if destination number is in number of destination lists
                    print("Error in Destination")#error statement
                    option = input("\nInput an option (MTT,MTF,MFT,U,R,H,Q): ").lower()#reprompt for option
                    continue
            if option[:3] == 'mtf':
                if int(option[-3]) <0 or int(option[-3]) >7:#if source number is in number of source lists
                    print("Error in Source.")#error statement
                    option = input("\nInput an option (MTT,MTF,MFT,U,R,H,Q): ").lower()#reprompt for option
                    continue
                if int(option[-1]) <0 or int(option[-1]) >3:#if destination number is in number of destination lists
                    print("Error in Destination")#error statement
                    option = input("\nInput an option (MTT,MTF,MFT,U,R,H,Q): ").lower()#reprompt for option
                    continue
            if option[:3] == 'mft':
                if int(option[-3]) <0 or int(option[-3]) >3:#if source number is in number of source lists
                    print("Error in Source.")#error statement
                    option = input("\nInput an option (MTT,MTF,MFT,U,R,H,Q): ").lower()#reprompt for option
                    continue
                if int(option[-1]) <0 or int(option[-1]) >7:#if destination number is in number of destination lists
                    print("Error in Destination")#error statement
                    option = input("\nInput an option (MTT,MTF,MFT,U,R,H,Q): ").lower()#reprompt for option
                    continue
            if len(option) != 7:#if option has valid number of characters for moves
                print( "Error in option:" ) #error statement
                option = input("\nInput an option (MTT,MTF,MFT,U,R,H,Q): ").lower()#reprompt for option
                continue
            else:
                move = str(option[:3]) #string the three move letters and uppercase them
                move = move.upper()
                option_list.append(move) #apppend move to option list
                option_list.append(int(option[-3]))#apppend source to option list
                option_list.append(int(option[-1]))#apppend destination to option list
                done == True #end loop
                return option_list
            


def main():
    moves_list = [] #empty moves list for undos
    print("\nWelcome to Streets and Alleys Solitaire.\n")  #header
    tableau,foundation = initialize() #initalize cards
    display(tableau, foundation) #display cards
    print(MENU) #print menu
    option = get_option()#prompt for option
    s,d = option[1],option[2] #set source and destination values
    
    while option[0]!= 'Q':
        if option[0] == "MTT": #for tab to tab
            valid = valid_tableau_to_tableau(tableau,s,d)
            if valid == False: #if  not valid
                print("Error in move: {} , {} , {}".format(option[0],option[1],option[2]))#error satement
                option = get_option()#reprompt for option
                s,d = option[1],option[2]#set source and destination values
            if valid== True:
                move_tableau_to_tableau(tableau,s,d) #make move
                win = check_for_win(foundation) #if win happens or not
                if win== True:
                    print("You won!\n") #print  win
                    display(tableau, foundation)#display cards
                    tableau,foundation = initialize()#initialize
                    print("\n- - - - New Game. - - - -\n")#new game header
                    display(tableau, foundation)#display cards
                    print(MENU)
                    moves_list.append(option)
                    option = get_option()#reprompt for option
                    try:
                        s,d = option[1],option[2]#set source and destination values
                    except:
                        continue
                if win == False:
                    display(tableau, foundation)#display cards
                    moves_list.append(option)
                    option = get_option()#reprompt for option
                    try:
                        s,d = option[1],option[2]#set source and destination values
                    except:
                        continue
                    
                    
        if option[0] == "MTF":
            valid = valid_tableau_to_foundation(tableau, foundation, s,d)
            if valid == False:#if  not valid
                print("Error in move: {} , {} , {}".format(option[0],option[1],option[2]))#error satement
                option = get_option()#reprompt for option
                s,d = option[1],option[2]#set source and destination values
            if valid== True:
                move_tableau_to_foundation(tableau, foundation, s,d)#make move
                win = check_for_win(foundation)#if win happens or not
                if win== True:
                    print("You won!\n")#print  win
                    display(tableau, foundation)#display cards
                    tableau,foundation = initialize()
                    print("\n- - - - New Game. - - - -\n") #new game header
                    display(tableau, foundation)#display cards
                    print(MENU)
                    moves_list.append(option)
                    option = get_option()#reprompt for option
                    try:
                        s,d = option[1],option[2]#set source and destination values
                    except:
                        continue
                if win == False:
                    display(tableau, foundation)#display cards
                    moves_list.append(option)
                    option = get_option()#reprompt for option
                    try:
                        s,d = option[1],option[2]#set source and destination values
                    except:
                        continue
        
        if option[0] == "MFT":
            valid = valid_foundation_to_tableau(tableau,foundation,s,d)
            if valid == False:
                print("Error in move: {} , {} , {}".format(option[0],option[1],option[2]))#error satement
                option = get_option()#reprompt for option
                s,d = option[1],option[2]#set source and destination values
            if valid== True:
                move_foundation_to_tableau(tableau,foundation,s,d)
                win = check_for_win(foundation)
                if win== True:
                    print("You won!\n")
                    display(tableau, foundation)#display cards
                    tableau,foundation = initialize()
                    print("\n- - - - New Game. - - - -\n")
                    display(tableau, foundation)#display cards
                    print(MENU)
                    moves_list.append(option)
                    option = get_option()#reprompt for option
                    try:
                        s,d = option[1],option[2]#set source and destination values
                    except:
                        continue
                if win == False:
                    display(tableau, foundation)#display cards
                    moves_list.append(option)
                    option = get_option()#reprompt for option
                    try:
                        s,d = option[1],option[2]#set source and destination values
                    except:
                        continue
            
        if option[0] == 'U':
            if moves_list == []: #previous moves list
                print("No moves to undo.")#error  statement
                option = get_option()#reprompt for option
                try:
                    s,d = option[1],option[2]#set source and destination values
                except:
                    continue
            if moves_list != []: #if list isnt empty
                move = moves_list.pop()
                if move[0] == 'MTT':
                    print("Undo:",move[0],move[1],move[2]) #undo header
                    des = tableau[move[1]] #new des
                    sor = tableau[move[2]]#new source
                    new_card = (sor[-1]) #card being undid
                    des.append(new_card) #append undo back
                    tableau[move[2]].pop() #remove undo from list
                    display(tableau, foundation) #display cards  
                    option = get_option()#reprompt for option
                    try:
                        s,d = option[1],option[2]#set source and destination values
                    except:
                        continue
                if move[0] == 'MTF':
                    print("Undo:",move[0],move[1],move[2])
                    des = tableau[move[1]]#new des
                    sor = foundation[move[2]]#new source
                    new_card = (sor[-1])#card being undid
                    des.append(new_card)#append undo back
                    foundation[move[2]].pop()#remove undo from list
                    display(tableau, foundation) #display cards  
                    option = get_option()#reprompt for option
                    try:
                        s,d = option[1],option[2]#set source and destination values
                    except:
                        continue
                if move[0] == 'MFT':
                    print("Undo:",move[0],move[1],move[2])
                    des = foundation[move[1]]#new des
                    sor = tableau[move[2]]#new source
                    new_card = (sor[-1])#card being undid
                    des.append(new_card)#append undo back
                    tableau[move[2]].pop()#remove undo from list
                    display(tableau, foundation)  #display cards 
                    option = get_option()#reprompt for option
                    try:
                        s,d = option[1],option[2]#set source and destination values
                    except:
                        continue
            

        
        if option[0] == 'R':
            tableau,foundation = initialize() #restart andinitalize tab and found
            display(tableau, foundation)#display cards
            option = get_option()#reprompt for option
            try:
                s,d = option[1],option[2]#set source and destination values
            except:
                continue
            moves_list.append(option) #append move to moves list
        
        if option[0] == 'H':
            print(MENU) #display menu
            option = get_option()#reprompt for option
            try:
                s,d = option[1],option[2]#set source and destination values
            except:
                continue
            moves_list.append(option)
            
 
        
    if option[0] == 'Q':
        print("Thank you for playing.")

    
if __name__ == '__main__':
     main()