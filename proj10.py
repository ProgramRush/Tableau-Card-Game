from cards import Card, Deck

MENU ='''Prompt the user for an option and check that the input has the 
       form requested in the menu, printing an error message, if not.
       Return:
    TT s d: Move card from end of Tableau pile s to end of pile d.
    TF s d: Move card from end of Tableau pile s to Foundation d.
    WT d: Move card from Waste to Tableau pile d.
    WF d: Move card from Waste to Foundation pile d.
    SW : Move card from Stock to Waste.
    R: Restart the game (after shuffling)
    H: Display this menu of choices
    Q: Quit the game        
    '''
def initialize():
    '''sets the intial of the deck by shuffling and putting some cards to waste '''
    stock = Deck()
    stock.shuffle()

    tableau = [[] for i in range(0, 7)]
    count = 0 

    for i in range(0, 7):
        count2 = count
        for j in range(count2, 7):
            card = stock.deal()
            if i != j:
                card.flip_card()
            tableau[j].append(card)
        count += 1
        
    foundation = [[] for i in range(0, 4)]
    waste = []
    waste.append(stock.deal())
    return tableau, stock, foundation, waste

def display(tableau, stock, foundation, waste):
    """ display the game setup """
    stock_top_card = "empty"
    found_top_cards = ["empty","empty","empty","empty"]
    waste_top_card = "empty"
    if len(waste):
        waste_top_card = waste[-1] 
    if len(stock):
        stock_top_card = "XX" #stock[-1]
    for i in range(4):
        if len(foundation[i]):
            found_top_cards[i] = foundation[i][-1]
    print()
    print("{:5s} {:5s} \t\t\t\t\t {}".format("stock","waste","foundation"))
    print("\t\t\t\t     ",end = '')
    for i in range(4):
        print(" {:5d} ".format(i+1),end = '')
    print()
    print("{:5s} {:5s} \t\t\t\t".format(str(stock_top_card), str(waste_top_card)), end = "")
    for i in found_top_cards:
        print(" {:5s} ".format(str(i)), end = "")
    print()
    print()
    print()
    print()
    print("\t\t\t\t\t{}".format("tableau"))
    print("\t\t ", end = '')
    for i in range(7):
        print(" {:5d} ".format(i+1),end = '')
    print()
    # calculate length of longest tableau column
    max_length = max([len(stack) for stack in tableau])
    for i in range(max_length):
        print("\t\t    ",end = '')
        for tab_list in tableau:
            # print card if it exists, else print blank
            try:
                print(" {:5s} ".format(str(tab_list[i])), end = '')
            except IndexError:
                print(" {:5s} ".format(''), end = '')
        print()
    print()
    

def stock_to_waste( stock, waste ):
    '''puts the intended stock, given in a parameter, to waste'''
    card = stock.deal()
    if card is None:
        return False
    waste.append(card)
    return True
    
       
def waste_to_tableau( waste, tableau, t_num ):
    '''takes the number of cards in waste and puts them in tableau'''
    if len(waste) == 0:
        return False
    card = waste[-1]
    if len(tableau[t_num]) == 0:
        if card.rank() == 13:
            tableau[t_num].append(waste.pop())
            return True
        return False
    tcard = tableau[t_num][-1]
    if tcard.suit() == 1 or tcard.suit() == 4:
        if card.suit() == 2 or card.suit() == 3 and card.rank()+1 == tcard.rank():
            tableau[t_num].append(waste.pop())
            return True
        return False
    if tcard.suit() == 2 or tcard.suit() == 3:
        if card.suit() == 1 or card.suit() == 4 and card.rank()+1 == tcard.rank():
            tableau[t_num].append(waste.pop())
            return True
        return False

def waste_to_foundation( waste, foundation, f_num ):
    '''takes the amt of cards from waste and puts them on foundation'''
    if len(waste) > 0:
        card = waste[-1]
        if len(foundation[f_num]) == 0:
            if card.rank() == 1:
                foundation[f_num].append(waste.pop())
                return True
            return False
        elif card.suit() == foundation[f_num][-1].suit() and card.rank() == foundation[f_num][-1].rank()+1:
            foundation[f_num].append(waste.pop())
            return True
    return False

def tableau_to_foundation( tableau, foundation, t_num, f_num ):
    '''Docstring'''
    if len(tableau[t_num]) > 0:
        card = tableau[t_num][-1]
        if len(foundation[f_num]) == 0:
            if card.rank() == 1:
                foundation[f_num].append(tableau[t_num].pop())
                if len(tableau[t_num]) > 0 and tableau[t_num][-1].is_face_up() == False:
                    tableau[t_num][-1].flip_card()
                return True
            return False
        elif card.suit() == foundation[f_num][-1].suit() and card.rank() == foundation[f_num][-1].rank()+1:
            foundation[f_num].append(tableau[t_num].pop())
            if len(tableau[t_num]) > 0 and tableau[t_num][-1].is_face_up() == False:
                tableau[t_num][-1].flip_card()
            return True
    return False
        

def tableau_to_tableau( tableau, t_num1, t_num2 ):
    '''takes the first number of cards from the tableau and then puts those cards to another tableau'''
    if tableau[t_num1] == 0:
        return False
    card = tableau[t_num1][-1]
    if len(tableau[t_num2]) == 0:
        if card.rank() == 13:
            tableau[t_num2].append(tableau[t_num1].pop())
            if len(tableau[t_num1]) > 0 and tableau[t_num1][-1].is_face_up() == False:
                tableau[t_num1][-1].flip_card()
            return True
        return False
    tcard = tableau[t_num2][-1]
    if tcard.suit() == 1 or tcard.suit() == 4:
        if card.suit() == 2 or card.suit() == 3 and card.rank()+1 == tcard.rank():
            tableau[t_num2].append(tableau[t_num1].pop())
            if len(tableau[t_num1]) > 0 and tableau[t_num1][-1].is_face_up() == False:
                tableau[t_num1][-1].flip_card()
            return True
        return False
    if tcard.suit() == 2 or tcard.suit() == 3:
        if card.suit() == 1 or card.suit() == 4 and card.rank()+1 == tcard.rank():
            tableau[t_num2].append(tableau[t_num1].pop())
            if len(tableau[t_num1]) > 0 and tableau[t_num1][-1].is_face_up() == False:
                tableau[t_num1][-1].flip_card()
            return True
        return False
    
    
def check_win (stock, waste, foundation, tableau):
    '''checks the cards in tableau, waste, and foundation to determine if you won'''
    if stock.is_empty() and len(waste) == 0:
        for i in range(0, 7):
            if len(tableau[i]) != 0:
                return False
        return True
    return False

def parse_option(in_str):
    '''Prompt the user for an option and check that the input has the 
           form requested in the menu, printing an error message, if not.
           Return:
        TT s d: Move card from end of Tableau pile s to end of pile d.
        TF s d: Move card from end of Tableau pile s to Foundation d.
        WT d: Move card from Waste to Tableau pile d.
        WF d: Move card from Waste to Foundation pile d.
        SW : Move card from Stock to Waste.
        R: Restart the game (after shuffling)
        H: Display this menu of choices
        Q: Quit the game        
        '''
    option_list = in_str.strip().split()
    
    opt_char = option_list[0][0].upper()
    
    if opt_char in 'RHQ' and len(option_list) == 1:  # correct format
        return [opt_char]
    
    if opt_char == 'S' and len(option_list) == 1:
        if option_list[0].upper() == 'SW':
            return ['SW']
    
    if opt_char == 'W' and len(option_list) == 2:
        if option_list[0].upper() == 'WT' or option_list[0].upper() == 'WF':
            dest = option_list[1] 
            if dest.isdigit():
                dest = int(dest)
                if option_list[0].upper() == 'WT' and (dest < 1 or dest > 7):
                    print("\nError in Destination")
                    return None
                if option_list[0].upper() == 'WF' and (dest < 1 or dest > 4):
                    print("\nError in Destination")
                    return None
                opt_str = option_list[0].strip().upper()
                return [opt_str,dest]
                               
    if opt_char == 'T' and len(option_list) == 3 and option_list[1].isdigit() \
        and option_list[2].isdigit():
        opt_str = option_list[0].strip().upper()
        if opt_str in ['TT','TF']:
            source = int(option_list[1])
            dest = int(option_list[2])
            # check for valid source values
            if opt_str in ['TT','TF'] and (source < 1 or source > 7):
                print("\nError in Source.")
                return None
            #elif opt_str == 'MFT' and (source < 0 or source > 3):
                #print("Error in Source.")
                #return None
            # source values are valid
            # check for valid destination values
            if (opt_str =='TT' and (dest < 1 or dest > 7)) \
                or (opt_str == 'TF' and (dest < 1 or dest > 4)):
                print("\nError in Destination")
                return None
            return [opt_str,source,dest]

    print("\nError in option:", in_str)
    return None   # none of the above


def main():   
    tableau, stock, foundation, waste = initialize()
    print(MENU)
    while True:
        display(tableau, stock, foundation, waste)
        inp = input("\nInput an option (TT,TF,WT,WF,SW,R,H,Q): ")
        option = parse_option(inp)
        if option is None:
            continue
        if option[0] == 'R':
            tableau, stock, foundation, waste = initialize()
        if option[0] == 'Q':
            break
        if option[0] == 'H':
            print(MENU)
        if option[0] == 'SW':
            if len(stock) > 0:
                stock_to_waste(stock, waste)
                #display(tableau, stock, foundation, waste)
            else:
                print("\nInvalid move!\n")
        if option[0] == 'TT':
            if tableau_to_tableau(tableau, option[1]-1, option[2]-1):
                continue
                #display(tableau, stock, foundation, waste)
            else:
                print("\nInvalid move!\n")
        if option[0] == 'TF':
            if tableau_to_foundation(tableau, foundation, option[1]-1, option[2]-1):
                if check_win(stock, waste, foundation, tableau):
                    print("You win!")
                    break
                else:
                    #display(tableau, stock, foundation, waste)
                    continue
            else:
                print("\nInvalid move!\n")
        if option[0] == 'WT':
            if waste_to_tableau(waste, tableau, option[1]-1):
                #display(tableau, stock, foundation, waste)
                continue
            else:
                print("\nInvalid move!\n")
        if option[0] == 'WF':
            if waste_to_foundation(waste, foundation, option[1]-1):
                if check_win(stock, waste, foundation, tableau):
                    print("You win!")
                    break
                else:
                    continue
                    #display(tableau, stock, foundation, waste)
            else:
                print("\nInvalid move!\n")
        


if __name__ == '__main__':
     main()