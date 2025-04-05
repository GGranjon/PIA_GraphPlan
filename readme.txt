DoPlan requiert uniquement un fichier "r_facts" comme argument.

PS : Dans les traces, pour une proposition, l'attribut "neg" indique si une proposition X est positive (X) ou négative (X_barre).
Cela est utilisé uniquement pour les propositions has_fuel, qui sont des booléens, mais les propositions négatives ne sont pas ajoutées
à la liste des propositions car elles ne servent pas (aucune méthode nécessite qu'une rocket n'ai pas de fuel). Ces propositions sont
uniquement utilisées pour le calcul des actions mutex. Donc cet attribut sera toujours à False dans la trace, mais est bien utilisé.