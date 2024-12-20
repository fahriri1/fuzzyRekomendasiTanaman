import numpy as np
import skfuzzy as fuzzy
from skfuzzy import control as ctrl

def initFuzzy():
    temperatur = ctrl.Antecedent(np.arange(10,40,1), 'temperatur')
    curah_hujan = ctrl.Antecedent(np.arange(200, 2600, 1), 'curah hujan')
    humid = ctrl.Antecedent(np.arange(10,100,1), 'humidity')

    temperatur['suhu dingin'] = fuzzy.trimf(temperatur.universe, [10, 15, 20])
    temperatur['Suhu sedikit dingin'] = fuzzy.trimf(temperatur.universe, [15, 20, 25])
    temperatur['Suhu sedang'] = fuzzy.trimf(temperatur.universe, [20, 25, 30])
    temperatur['Suhu sedikit panas'] = fuzzy.trimf(temperatur.universe, [25, 30, 35])
    temperatur['Suhu panas'] = fuzzy.trimf(temperatur.universe, [30, 35, 40])

    curah_hujan['Kering'] = fuzzy.trimf(curah_hujan.universe, [200, 600, 1000])
    curah_hujan['Jarang hujan'] = fuzzy.trimf(curah_hujan.universe, [600, 1000, 1400])
    curah_hujan['Hujan'] = fuzzy.trimf(curah_hujan.universe, [1000, 1400, 1800])
    curah_hujan['Sering hujan'] = fuzzy.trimf(curah_hujan.universe, [1400, 1800, 2200])
    curah_hujan['Hujan lebat'] = fuzzy.trimf(curah_hujan.universe, [1800, 2200, 2600])

    humid['Kering'] = fuzzy.trimf(humid.universe, [10, 25, 40])
    humid['Sedikit lembab'] = fuzzy.trimf(humid.universe, [25, 40, 55])
    humid['Lembab'] = fuzzy.trimf(humid.universe, [40, 55, 70])
    humid['Lebih lembab'] = fuzzy.trimf(humid.universe, [55, 70, 85])
    humid['Sangat lembab'] = fuzzy.trimf(humid.universe, [70, 85, 100])

    jagung = ctrl.Consequent(np.arange(0,100,1), 'jagung')
    kentang = ctrl.Consequent(np.arange(0,100,1), 'kentang')
    pisang = ctrl.Consequent(np.arange(0,100,1), 'pisang')

    jagung['Tidak sesuai'] = fuzzy.trimf(jagung.universe, [0, 20, 40])
    jagung['Sesuai marginal'] = fuzzy.trimf(jagung.universe, [20, 40, 60])
    jagung['Cukup sesuai'] = fuzzy.trimf(jagung.universe, [40, 60, 80])
    jagung['Sangat sesuai'] = fuzzy.trimf(jagung.universe, [60, 80, 100])

    kentang['Tidak sesuai'] = fuzzy.trimf(kentang.universe, [0, 20, 40])
    kentang['Sesuai marginal'] = fuzzy.trimf(kentang.universe, [20, 40, 60])
    kentang['Cukup sesuai'] = fuzzy.trimf(kentang.universe, [40, 60, 80])
    kentang['Sangat sesuai'] = fuzzy.trimf(kentang.universe, [60, 80, 100])

    pisang['Tidak sesuai'] = fuzzy.trimf(pisang.universe, [0, 20, 40])
    pisang['Sesuai marginal'] = fuzzy.trimf(pisang.universe, [20, 40, 60])
    pisang['Cukup sesuai'] = fuzzy.trimf(pisang.universe, [40, 60, 80])
    pisang['Sangat sesuai'] = fuzzy.trimf(pisang.universe, [60, 80, 100])

    jagung1 = ctrl.Rule(temperatur['Suhu sedang'] & curah_hujan['Jarang hujan'] & humid['Sangat lembab'], jagung['Sangat sesuai'])
    jagung2 = ctrl.Rule(temperatur['Suhu sedikit panas'] & curah_hujan['Kering'] & humid['Lebih lembab'], jagung['Cukup sesuai'])
    jagung3 = ctrl.Rule(temperatur['Suhu sedikit panas'] & curah_hujan['Kering'] & humid['Lembab'], jagung['Sesuai marginal'])
    jagung4 = ctrl.Rule(temperatur['Suhu panas'] & curah_hujan['Kering'] & humid['Kering'], jagung['Tidak sesuai'])

    kentang1 = ctrl.Rule(temperatur['Suhu sedikit dingin'] & curah_hujan['Hujan lebat'] & humid['Sangat lembab'], kentang['Sangat sesuai'])
    kentang2 = ctrl.Rule(temperatur['Suhu sedang'] & curah_hujan['Sering hujan'] & humid['Lebih lembab'], kentang['Cukup sesuai'])
    kentang3 = ctrl.Rule(temperatur['Suhu sedikit panas'] & curah_hujan['Hujan'] & humid['Lebih lembab'], kentang['Sesuai marginal'])
    kentang4 = ctrl.Rule(temperatur['Suhu panas'] & curah_hujan['Jarang hujan'] & humid['Lembab'], kentang['Tidak sesuai'])

    pisang1 = ctrl.Rule(temperatur['Suhu sedikit dingin'] & curah_hujan['Hujan lebat'] & humid['Sangat lembab'], pisang['Sangat sesuai'])
    pisang2 = ctrl.Rule(temperatur['Suhu sedikit panas'] & curah_hujan['Sering hujan'] & humid['Lebih lembab'], pisang['Cukup sesuai'])
    pisang3 = ctrl.Rule(temperatur['Suhu sedikit panas'] & curah_hujan['Hujan'] & humid['Lebih lembab'], pisang['Sesuai marginal'])
    pisang4 = ctrl.Rule(temperatur['Suhu panas'] & curah_hujan['Jarang hujan'] & humid['Lembab'], pisang['Tidak sesuai'])

    tipping_ctrl = ctrl.ControlSystem([jagung1, jagung2, jagung3, jagung4, 
                                    kentang1, kentang2, kentang3, kentang4, 
                                    pisang1, pisang2, pisang3, pisang4])
    tipping = ctrl.ControlSystemSimulation(tipping_ctrl)
    return tipping

def calcFuzzy(tempt_, rain_, humid_):
    tipping = initFuzzy()

    tipping.input['temperatur'] = tempt_
    tipping.input['curah hujan'] = rain_
    tipping.input['humidity'] = humid_

    tipping.compute()

    try:
        jagung = int(tipping.output['jagung'])
    except KeyError:
        jagung = 0

    try:
        kentang = int(tipping.output['kentang'])
    except KeyError:
        kentang = 0

    try:
        pisang = int(tipping.output['pisang'])
    except KeyError:
        pisang = 0

    
    print("tingkat kecocokan tanaman jagung:", jagung, "%")
    print("tingkat kecocokan tanaman kentang:", kentang, "%")
    print("tingkat kecocokan tanaman pisang:", pisang, "%")
    
    return pisang, kentang, jagung