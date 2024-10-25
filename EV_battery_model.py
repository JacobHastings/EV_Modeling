#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
import matplotlib.pyplot as plt
import numpy as np


def charging_power_CC_CV(battery):
    if battery["Q"] / battery["Q_nom"] >= (battery["max_Q_pct"]/100):
        battery["P_battery"] = 0
        return battery
    
    term1 = (battery["K"] * battery["Q_nom"])/(battery["Q_nom"]-battery["Q"])
    term2 = battery["A"] * (math.exp(-1*battery["B"]*battery["Q"]))
    V_oc = battery["V_0"] - term1 + term2
    
    # Q = battery["Q_nom"] - battery["Q"]
    # term1 = (battery["K"] * battery["Q_nom"])/(battery["Q_nom"]-Q)
    # term2 = battery["A"] * (math.exp(-1*battery["B"]*Q))
    # V_oc = battery["V_0"] - term1 + term2
    
    V_pack = battery["V_pack"]
    
    # CC Region
    # CC switches to CV at approx 90% charge
    if battery["Q"] / battery["Q_nom"] < 0.9:
        # "What pack voltage gives the goal 20A CC setting?"
        battery["V_pack"] = V_oc + (battery["R_eq"] * battery["I"])
        # battery terminal voltage
        battery["V_t"] = V_oc + (battery["R_i"] * battery["I"])
        P_dc = battery["V_pack"] * battery["I"]
        battery["P_battery"] = P_dc * battery["cells"]
    # CV Region
    else:
        #Constant voltage set to 4.25 for CV mode
        V_pack = battery["V_pack"]
        #What current do you get from the voltage used in the CV mode
        I = (V_pack - V_oc) / (battery["R_eq"])
        battery["V_t"] = V_oc + (battery["R_i"] * I)
        P_dc = V_pack * I
        battery["P_battery"] = P_dc * battery["cells"]
    return battery
    
    

battery_specs = {
    "Q_nom": 40,
    "Q": 24,
    "max_Q_pct": 100,
    "V_0": 3.5,
    "R_eq": 1.1,
    "R_i": 0.01,
    "I": 20,
    "Vc": 4.25,
    "V_t": 0,
    "V_pack": 0,
    "eff": 0.88,
    "A": 0.2,
    "B": 0.375,
    "K": 0.025,
    "P_battery": 0,
    "cells": 110,
    "modules": 11
    }  

flag_power_v_charge = 1
flag_charge_pct = 1


##############################################################################
#                          Power vs Charge                                   #
##############################################################################
if flag_power_v_charge:
    intervals = 30
    
    
    if flag_charge_pct:
        charge = np.linspace((battery_specs["Q_nom"]*0),(battery_specs["Q_nom"]-(battery_specs["Q_nom"]/intervals))*0.92,num=intervals)
    else:
        charge = np.linspace(0,battery_specs["Q_nom"],num=intervals)
    power = np.zeros_like(charge)
    
    for i in range(intervals):
        battery_specs["Q"] = charge[i]
        battery_specs = charging_power_CC_CV(battery_specs)
        power[i] = battery_specs["P_battery"]
        
    fig_kW_v_kWh = plt.figure()
    if flag_charge_pct:
        plt.plot(100*charge/battery_specs["Q_nom"],power/1000)
    else:
        plt.plot((charge*battery_specs["cells"]*battery_specs["V_0"])/1000,(power/1000))
    plt.title("Battery Power Versus Charge")
    if flag_charge_pct:
        plt.xlabel("Charge (%)")
    else:
        plt.xlabel("Charge (kWh)")
    plt.ylabel("Power to Battery (kW)")
    if flag_charge_pct:
        plt.xlim([15,95])
    plt.grid()
    # plt.ylim([0,10])


##############################################################################
#                          Time Simulation (V)                               #
##############################################################################


start_charge = 0.2
time_intervals = 500
max_time = 60*150
V_packs = np.arange(430,432,2)

time = np.linspace(0,max_time,time_intervals)
time_power = np.zeros([len(V_packs),time_intervals])
time_charge = np.zeros_like(time_power)
    



