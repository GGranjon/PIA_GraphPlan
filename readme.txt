DoPlan requiert uniquement un fichier "r_facts" comme argument, pas de "r_ops.txt".

PS : La proposition negative de has_fuel n'est jamais ajouté à la liste des propositions car elle n'est jamais utilisée
(aucune action ne requiert en précondition de ne pas avoir de fuel). Cette proposition est en revanche bien utilisée dans
la recherche des actions mutex. Il serait très simple (instantané) de l'ajouter, mais cela rajouterait des calculs
inutiles.

PS2 : La propagation arrière pour trouver une solution est faite en parallèle, afin d'accélerer le processus. De plus, le programme
calcul d'abord toute les combinaisons possibles, pour ensuite voir si une convient. La trace peut donc être un peu difficile à lire
sur ces étapes, puisqu'on continue les recherches même si une solution a été trouvée.