def es_mayuscula(c):
    return 'A' <= c <= 'Z'

def es_digito(c):
    return c in '0123456789'

def validar_moneda(nro_cod):
    nro_cod = nro_cod.strip()
    ars = 0
    usd = 0
    jpy = 0
    eur = 0
    gbp = 0
    moneda = None

    if "ARS" in nro_cod:
        ars = 1
        moneda = "ARS"

    if "USD" in nro_cod:
        usd = 1
        moneda = "USD"

    if "JPY" in nro_cod:
        jpy = 1
        moneda = "JPY"

    if "EUR" in nro_cod:
        eur = 1
        moneda = "EUR"

    if "GBP" in nro_cod:
        gbp = 1
        moneda = "GBP"

    suma = ars + usd + jpy + eur + gbp

    if suma > 1 or suma == 0:
        moneda = "Moneda no valida."

    return moneda

def validar_numero_orden(num_codigo):
    num_codigo = num_codigo.strip()
    if num_codigo == '':
        return False

    valido = False
    for c in num_codigo:
        if es_mayuscula(c) or es_digito(c):
            valido = True
        elif c != '-':
            return False

    return valido

def calcular_monto_base_1(monto_nominal):
    return monto_nominal - ((monto_nominal * 9) // 100)

def calcular_monto_base_2(monto_nominal):
    if monto_nominal < 50000:
        return monto_nominal
    elif 50000 <= monto_nominal < 80000:
        return monto_nominal - ((monto_nominal * 5) // 100)
    else:
        return monto_nominal - ((monto_nominal * 7.8) // 100)

def calcular_monto_base_3(monto_nominal):
    MONTO_FIJO = 100
    comision = 0
    if monto_nominal > 25000:
        comision = (monto_nominal * 6) // 100
    return monto_nominal - (MONTO_FIJO + comision)

def calcular_monto_base_4(monto_nominal):
    if monto_nominal <= 100000:
        return monto_nominal - 500
    else:
        return monto_nominal - 1000

def calcular_monto_base_5(monto_nominal):
    comision = 0
    if monto_nominal >= 500000:
        comision = (monto_nominal * 7) // 100
    if comision > 50000:
        comision = 50000
    return monto_nominal - comision

def calcular_monto_base_7(monto_nominal):
    comision = 0
    if monto_nominal <= 75000:
        comision = 3000
    else:
        comision = ((monto_nominal - 75000) * 5) // 100
    if comision > 10000:
        comision = 10000
    return monto_nominal - comision

def calcular_monto_base(monto_nominal, n_algoritmo):
    if n_algoritmo == 1:
        return calcular_monto_base_1(monto_nominal)
    elif n_algoritmo == 2:
        return calcular_monto_base_2(monto_nominal)
    elif n_algoritmo == 3:
        return calcular_monto_base_3(monto_nominal)
    elif n_algoritmo == 4:
        return calcular_monto_base_4(monto_nominal)
    elif n_algoritmo == 5:
        return calcular_monto_base_5(monto_nominal)
    elif n_algoritmo == 7:
        return calcular_monto_base_7(monto_nominal)
    else:
        return monto_nominal

def calcular_monto_final_1(monto_base):
    impuesto = 0
    if monto_base > 300000:
        excedente = monto_base - 300000
        impuesto = (excedente * 25) // 100
    return monto_base - impuesto

def calcular_monto_final_2(monto_base):
    if monto_base < 50000:
        impuesto = 50
    else:
        impuesto = 100
    return monto_base - impuesto

def calcular_monto_final_3(monto_base):
    impuesto = (monto_base * 3) // 100
    return monto_base - impuesto

def calcular_monto_final(monto_base, n_algoritmo):
    if n_algoritmo == 1:
        return calcular_monto_final_1(monto_base)
    elif n_algoritmo == 2:
        return calcular_monto_final_2(monto_base)
    elif n_algoritmo == 3:
        return calcular_monto_final_3(monto_base)
    else:
        return monto_base

def calcular_promedio_entero(suma,cant):
    if cant > 0:
        return suma // cant
    return 0

def calcular_porcentaje_entero(cant,total):
    if total > 0:
        return (cant * 100) // total
    return 0

def main():
    archivo = open("ordenes.txt")
    timestamp = archivo.readline()
    linea = archivo.readline()

    cant_minvalida,cant_binvalido,cant_oper_validas,suma_mf_validas = 0,0,0,0
    cant_ARS,cant_USD,cant_EUR,cant_GBP,cant_JPY = 0,0,0,0,0
    my_dif,cod_my,mont_nom_my,mont_fin_my = None,None,None,None
    nom_primer_benef,cant_nom_primer_benef = None,0
    total_ordenes = 0
    sum_ARS = 0
    cant_ARS_validas = 0

    while linea != "":
        nombre_destinatario = linea[0:20].strip()
        numero_codigo = linea[20:30].strip()
        codigo_orden = linea[30:40].strip()
        monto_nominal = float(linea[40:50].strip())
        id_algoritmo_comision = int(linea[50:52].strip())
        id_algoritmo_impuesto = int(linea[52:54].strip())

        moneda = validar_moneda(codigo_orden)
        destinatario_ok = validar_numero_orden(numero_codigo)

        total_ordenes += 1

        #5. El nombre del beneficiario de la primera operacion del archivo (r13), y la cantidad de veces que ese mismo beneficiario aparecio en el archivo (r14).
        if nom_primer_benef is None:
            nom_primer_benef = nombre_destinatario
            cant_nom_primer_benef = 1
        elif nom_primer_benef == nombre_destinatario:
            cant_nom_primer_benef += 1

        monto_base = calcular_monto_base(monto_nominal, id_algoritmo_comision)
        monto_final = calcular_monto_final(monto_base, id_algoritmo_impuesto)

        # 4. El codigo de la orden de pago (r10),el monto nominal (r11) y el monto final (r12) de la operacion que tenga la mayor diferencia entre el monto nominal y el monto final (monto_nominal - monto_final)(si hubiera mas de una operacion con la misma diferencia mayor, informar el codigo de la orden de la primera de ellas). Aqui deben ser consideradas TODAS las ordenes de pago (tanto validas como invalidas...)
        dif = monto_nominal - monto_final
        if my_dif is None or dif > my_dif: #no considero el caso en que sea = asique siempre deja la primera
            my_dif = dif
            cod_my = codigo_orden
            mont_nom_my = monto_nominal
            mont_fin_my = monto_final

        if moneda == 'Moneda no valida.':
            #1. cantidad de operaciones invalidas que hay en el lote por moneda no autorizada (r1)
            cant_minvalida += 1
        elif not destinatario_ok:
            #1. cantidad de operaciones invalidas que hay en el lote por un destinatario mal identificado (r2)
            cant_binvalido += 1
        else:
            #2. La cantidad de operaciones validas (r3)
            cant_oper_validas += 1
            #2. la suma de todos los montos finales de estas operaciones validas (r4).
            suma_mf_validas += monto_final

            #El monto final promedio, pagado entre todas las ordenes validas (en moneda y en beneficiario) emitidas en moneda ARS (r16).
            if moneda == 'ARS':
                sum_ARS += monto_final
                cant_ARS_validas += 1

        if moneda != 'Moneda no valida.':
            #3. La cantidad de operaciones para cada una de las cinco monedas validas en este modelo de trabajo (r5, r6, r7, r8 y r9). Si la orden tiene moneda valida, debe contarse sin importar si el beneficiario era incorrecto.
            if moneda == 'ARS':
                cant_ARS += 1
            elif moneda == 'USD':
                cant_USD += 1
            elif moneda == 'EUR':
                cant_EUR += 1
            elif moneda == 'GBP':
                cant_GBP += 1
            elif moneda == 'JPY':
                cant_JPY += 1

        linea = archivo.readline()

    archivo.close()
    #El porcentaje que la cantidad de operaciones invalidas (por cualquier motivo) representa sobre la cantidad total de ordenes del archivo (r15).
    porcentaje = calcular_porcentaje_entero((total_ordenes - cant_oper_validas),total_ordenes)

    #El monto final promedio, pagado entre todas las ordenes validas (en moneda y en beneficiario) emitidas en moneda ARS (r16).
    promedio = calcular_promedio_entero(sum_ARS,cant_ARS_validas)

    print(' (r1) - Cantidad de ordenes invalidas - moneda no autorizada:', cant_minvalida)
    print(' (r2) - Cantidad de ordenes invalidas - beneficiario mal identificado:', cant_binvalido)
    print(' (r3) - Cantidad de operaciones validas:', cant_oper_validas)
    print(' (r4) - Suma de montos finales de operaciones validas:', round(suma_mf_validas,2))
    print(' (r5) - Cantidad de ordenes para moneda ARS:', cant_ARS)
    print(' (r6) - Cantidad de ordenes para moneda USD:', cant_USD)
    print(' (r7) - Cantidad de ordenes para moneda EUR:', cant_EUR)
    print(' (r8) - Cantidad de ordenes para moneda GBP:', cant_GBP)
    print(' (r9) - Cantidad de ordenes para moneda JPN:', cant_JPY)
    print('(r10) - Codigo de la orden de pago con mayor diferencia nominal - final:', cod_my)
    print('(r11) - Monto nominal de esa misma orden:', mont_nom_my)
    print('(r12) - Monto final de esa misma orden:', mont_fin_my)
    print('(r13) - Nombre del primer beneficiario del archivo:', nom_primer_benef)
    print('(r14) - Cantidad de veces que apareció ese mismo nombre:', cant_nom_primer_benef)
    print('(r15) - Porcentaje de operaciones inválidas sobre el total:', porcentaje)
    print('(r16) - Monto final promedio de las ordenes validas en moneda ARS:', promedio)

main()