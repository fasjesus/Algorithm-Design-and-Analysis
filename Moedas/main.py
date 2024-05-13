def TrocoOtimo(moedas, troco):
    quantidade = [0] * (troco + 1)
    ultima = [0] * (troco + 1)

    for c in range(1, troco + 1):
        quantidade_provisoria = c
        ultima_provisoria = 1

        for j in range(len(moedas)):
            if moedas[j] > c:
                continue
            if quantidade[c - moedas[j]] + 1 <= quantidade_provisoria:
                quantidade_provisoria = quantidade[c - moedas[j]] + 1
                ultima_provisoria = moedas[j]

        quantidade[c] = quantidade_provisoria
        ultima[c] = ultima_provisoria

    return quantidade, ultima

moedas = [1, 3, 13, 15, 18]
troco_maximo = 45

quantidades, ultimas_moedas = TrocoOtimo(moedas, troco_maximo)

with open("Moedas/output.txt", "w") as file:
    file.write("{:<10} | {:<10} | {:<12} | {}\n".format("Troco", "Quantidade", "Ultima Moeda", "Moedas Utilizadas"))
    for troco in range(troco_maximo + 1):
        quantidade_minima = quantidades[troco]
        moedas_utilizadas = []

        # Reconstruir as moedas utilizadas a partir das últimas moedas
        troco_atual = troco
        while troco_atual > 0:
            moedas_utilizadas.append(ultimas_moedas[troco_atual])
            troco_atual -= ultimas_moedas[troco_atual]

        if moedas_utilizadas:
            file.write("{:<10}  {:<10}  {:<12}  {}\n".format(troco, quantidade_minima, moedas_utilizadas[-1], moedas_utilizadas))
        else:
            file.write("{:<10}  {:<10}  {:<12}  {}\n".format(troco, quantidade_minima, "-", "Sem moedas utilizadas"))