"""Desk-Mate: Schaltung der drei Platinen als Daten (Spec §2.2–2.4, pins.h).

Jedes Teil: (ref, lib, symbol, value, footprint, {pin: netz | None}, pcb={x, y, rot}).
PCB-Koordinaten = Mitte des Courtyards in mm, Ursprung links oben, Y nach unten.
Netznamen = pins.h ohne PIN_. None = No-Connect-Kreuz.
"""
from sch import make_custom_symbol

# ---------------------------------------------------------------- Modul-Maße (Recherche 2026-08-27, siehe vault/Hardware/Module-Masse.md)
DEVKIT_ROW_SPACING = 22.86   # ESP32-S3-DevKitC-1: Abstand der beiden Buchsenreihen
DEVKIT_W, DEVKIT_L = 25.5, 63.5
DRV8833_ROW_SPACING = 10.16  # Pololu #2130: 0,5" breit, Reihen 0,4" auseinander
DRV8833_W, DRV8833_L = 12.7, 20.3
DEVKIT_OUTLINE_DY = 3.30     # Pinfeld sitzt 3,3 mm zum Antennenende hin (Pin 1 = Antennenende, 1,40 mm vom Rand)
# MT3608-Modul: Lochraster nicht 2,54-kompatibel (6,45–6,8 / 30,5–31 mm) -> Modul per 4 Drähten an Stiftleiste (ponytail)

RAX = 'Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal'
C100N = 'Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm'
CP1000 = 'Capacitor_THT:CP_Radial_D10.0mm_P5.00mm'
CP470 = 'Capacitor_THT:CP_Radial_D8.0mm_P3.50mm'
CP100 = 'Capacitor_THT:CP_Radial_D6.3mm_P2.50mm'
CP10 = 'Capacitor_THT:CP_Radial_D5.0mm_P2.00mm'   # Reichelt 10 µF D5 hat RM 2,0
JP2O = ('Jumper', 'SolderJumper_2_Open', 'Jumper:SolderJumper-2_P1.3mm_Open_RoundedPad1.0x1.5mm')
JP2B = ('Jumper', 'SolderJumper_2_Bridged', 'Jumper:SolderJumper-2_P1.3mm_Bridged_RoundedPad1.0x1.5mm')
JP3 = ('Jumper', 'SolderJumper_3_Bridged12', 'Jumper:SolderJumper-3_P1.3mm_Bridged12_RoundedPad1.0x1.5mm_NumberLabels')
HOLE = ('Mechanical', 'MountingHole', 'MountingHole:MountingHole_3.2mm_M3')
TP = ('Connector', 'TestPoint', 'TestPoint:TestPoint_THTPad_1.5x1.5mm_Drill0.7mm')
MKDS4 = 'TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-4-5.08_1x04_P5.08mm_Horizontal'   # Reichelt MKDS 1,5 4 5,08
SOCK = 'Connector_PinSocket_2.54mm:PinSocket_1x%02d_P2.54mm_Vertical'
HDR = 'Connector_PinHeader_2.54mm:PinHeader_1x%02d_P2.54mm_Vertical'
IDC = 'Connector_IDC:IDC-Header_2x15_P2.54mm_Vertical'
IDC10 = 'Connector_IDC:IDC-Header_2x05_P2.54mm_Vertical'

# ---------------------------------------------------------------- eigene Symbole
DEVKIT_J1 = ['3V3', '3V3', 'EN', 'IO4', 'IO5', 'IO6', 'IO7', 'IO15', 'IO16', 'IO17', 'IO18', 'IO8', 'IO3', 'IO46',
             'IO9', 'IO10', 'IO11', 'IO12', 'IO13', 'IO14', '5V', 'GND']
DEVKIT_J3 = ['GND', 'TXD0/IO43', 'RXD0/IO44', 'IO1', 'IO2', 'IO42', 'IO41', 'IO40', 'IO39', 'IO38', 'IO37', 'IO36',
             'IO35', 'IO0', 'IO45', 'IO48', 'IO47', 'IO21', 'IO20', 'IO19', 'GND', 'GND']
DEVKIT_PINS = [(str(i + 1), n, 'L', i, 'power_in' if n in ('5V',) else 'passive' if n in ('3V3', 'GND') else 'bidirectional')
               for i, n in enumerate(DEVKIT_J1)] + \
              [(str(i + 23), n, 'R', i, 'passive' if n == 'GND' else 'bidirectional') for i, n in enumerate(DEVKIT_J3)]

# Pololu DRV8833 (#2130), Draufsicht, GND-Ende oben: links 1–8, rechts 9–16 (Pololu-Pinout-Bild 0J3866)
DRV8833_ROW1 = ['GND', 'VMM', 'BIN1', 'BIN2', 'AIN2', 'AIN1', 'nSLEEP', 'nFAULT']
DRV8833_ROW2 = ['GND2', 'VIN', 'BOUT1', 'BOUT2', 'AOUT2', 'AOUT1', 'AISEN', 'BISEN']
DRV8833_PINS = [(str(i + 1), n, 'L', i, 'passive') for i, n in enumerate(DRV8833_ROW1)] + \
               [(str(i + 9), n, 'R', i, 'passive') for i, n in enumerate(DRV8833_ROW2)]

MT3608_PINS = [('1', 'VIN+', 'L', 0, 'passive'), ('2', 'VIN-', 'L', 1, 'passive'),
               ('3', 'VOUT+', 'R', 0, 'passive'), ('4', 'VOUT-', 'R', 1, 'passive')]

CUSTOM_SYMBOLS = {
    'ESP32-S3-DevKitC-1': make_custom_symbol('ESP32-S3-DevKitC-1', DEVKIT_PINS, width=25.4, ref_prefix='U',
                                             desc='Espressif ESP32-S3-DevKitC-1 N16R8, gesteckt (2x 1x22 Buchsenleiste)'),
    'DRV8833_Breakout': make_custom_symbol('DRV8833_Breakout', DRV8833_PINS, width=20.32, ref_prefix='U',
                                           desc='Pololu DRV8833 Dual Motor Driver Carrier #2130 (Sockel 2x 1x8)'),
    'MT3608_Module': make_custom_symbol('MT3608_Module', MT3608_PINS, width=17.78, ref_prefix='U',
                                        desc='MT3608 Step-up-Modul, VM-Boost (optional)'),
}

IDC_NETS = {1: '5V', 2: '5V', 3: 'GND', 4: 'GND', 5: '3V3', 6: '3V3', 7: 'MOT1A', 8: 'MOT1B', 9: 'MOT2A', 10: 'MOT2B',
            11: 'MOT3A', 12: 'MOT3B', 13: 'MOT4A', 14: 'MOT4B', 15: 'GND', 16: 'GND', 17: 'FADER1_WIPER',
            18: 'FADER2_WIPER', 19: 'FADER3_WIPER', 20: 'FADER4_WIPER', 21: 'GND', 22: 'I2C_SDA', 23: 'I2C_SCL',
            24: 'IO_INT', 25: 'SPI_MOSI', 26: 'SPI_SCK', 27: 'SPI_DC', 28: 'CS_BELLY', 29: 'DISP_RST', 30: 'GND'}
IDC_NETS = {str(k): v for k, v in IDC_NETS.items()}
# Augen-Kabel = IDC 2x5 + 10 Adern Flachband: GND zwischen SCK und MOSI (Adern liegen in Pin-Reihenfolge nebeneinander)
EYE_CABLE = {'1': '3V3', '2': 'GND', '3': 'SPI_SCK', '4': 'GND', '5': 'SPI_MOSI', '6': 'GND', '7': 'SPI_DC',
             '8': 'CS_EYE_L', '9': 'CS_EYE_R', '10': 'DISP_RST'}


def r(ref, val, n1, n2, x, y, rot=0):
    return (ref, 'Device', 'R', val, RAX, {'1': n1, '2': n2}, dict(x=x, y=y, rot=rot))


def c(ref, val, n1, n2, x, y, rot=0, fp=C100N):
    return (ref, 'Device', 'C', val, fp, {'1': n1, '2': n2}, dict(x=x, y=y, rot=rot))


def cp(ref, val, pos, neg, x, y, rot=0, fp=CP100):
    return (ref, 'Device', 'C_Polarized', val, fp, {'1': pos, '2': neg}, dict(x=x, y=y, rot=rot))


def jp2(ref, kind, val, a, b, x, y, rot=0):
    return (ref, kind[0], kind[1], val, kind[2], {'1': a, '2': b}, dict(x=x, y=y, rot=rot))


def jp3(ref, val, a, common, b, x, y, rot=0):
    return (ref, JP3[0], JP3[1], val, JP3[2], {'1': a, '2': common, '3': b}, dict(x=x, y=y, rot=rot))


def hole(ref, x, y):
    return (ref, HOLE[0], HOLE[1], 'M3', HOLE[2], {}, dict(x=x, y=y, rot=0))


def tp(ref, net, x, y):
    return (ref, TP[0], TP[1], net, TP[2], {'1': net}, dict(x=x, y=y, rot=0))


def conn(ref, n, value, fp, nets, x, y, rot=0, lib='Connector_Generic', dnp=False):
    return (ref, lib, f'Conn_01x{n:02d}', value, fp, {str(i + 1): nets[i] for i in range(n)}, dict(x=x, y=y, rot=rot), dnp)


def devkit_nets():
    m = {'3V3': None, 'EN': 'RST_N', 'IO4': 'FADER3_WIPER', 'IO5': 'FADER4_WIPER', 'IO6': 'FADER1_PWM',
         'IO7': 'FADER1_DIR', 'IO15': 'SERVO_TILT', 'IO16': 'SPI_MOSI', 'IO17': 'I2C_SDA', 'IO18': 'I2C_SCL',
         'IO8': 'FADER2_PWM', 'IO3': None, 'IO46': None, 'IO9': 'FADER2_DIR', 'IO10': 'FADER3_PWM',
         'IO11': 'FADER3_DIR', 'IO12': 'FADER4_PWM', 'IO13': 'FADER4_DIR', 'IO14': 'SERVO_PAN', '5V': '5V',
         'GND': 'GND', 'TXD0/IO43': None, 'RXD0/IO44': None, 'IO1': 'FADER1_WIPER',
         'IO2': 'FADER2_WIPER', 'IO42': 'CS_EYE_L', 'IO41': 'CS_BELLY', 'IO40': 'SPI_DC', 'IO39': 'SPI_SCK',
         'IO38': 'WS2812_DATA', 'IO37': None, 'IO36': None, 'IO35': None, 'IO0': 'BOOT_N', 'IO45': None,
         'IO48': 'PSU_SENSE', 'IO47': 'CS_EYE_R', 'IO21': 'IO_INT', 'IO20': None, 'IO19': None}
    return {num: m[name] for num, name, *_ in DEVKIT_PINS}


def drv_nets(a_pwm, a_dir, b_pwm, b_dir, aout, bout):
    m = {'VIN': 'VM', 'GND': 'GND', 'AOUT1': aout[0], 'AOUT2': aout[1], 'BOUT2': bout[1], 'BOUT1': bout[0],
         'VMM': None, 'GND2': 'GND', 'nSLEEP': '3V3', 'nFAULT': None, 'AIN1': a_pwm, 'AIN2': a_dir,
         'BIN2': b_dir, 'BIN1': b_pwm, 'AISEN': None, 'BISEN': None}
    return {num: m[name] for num, name, *_ in DRV8833_PINS}


# ================================================================ MAINBOARD 100 x 100 (Rueckwand = oben, y=0)
MAIN_W, MAIN_H = 100.0, 100.0
MAINBOARD = {
    'name': 'mainboard', 'title': 'Desk-Mate Mainboard (Base)', 'w': MAIN_W, 'h': MAIN_H,
    'sections': [
        ('Versorgung: J1 (Schraubklemme <- USB-C-Breakout in der Rueckwand, CC1/CC2 je 5k1) 5V/3A -> Polyfuse -> SB540 -> 5V-Rail; LD1117V33 fuer Peripherie; PSU_SENSE vor der Diode (10k/15k -> 3,0 V)', [
            conn('J1', 4, 'USB-C-Breakout 5V/3A (VBUS GND CC1 CC2)', MKDS4, ['VBUS', 'GND', 'CC1', 'CC2'], 52, 6),
            r('R1', '5k1', 'CC1', 'GND', 40, 14.5), r('R2', '5k1', 'CC2', 'GND', 40, 18.5),
            ('F1', 'Device', 'Polyfuse', '3A RXEF300', 'deskmate:Polyfuse_Radial_P5.08mm',
             {'1': 'VBUS', '2': 'VBUS_F'}, dict(x=55, y=15.5, rot=0)),
            ('D1', 'Device', 'D_Schottky', 'SB540', 'Diode_THT:D_DO-201_P15.24mm_Horizontal',
             {'2': 'VBUS_F', '1': '5V'}, dict(x=57, y=21, rot=0)),
            r('R3', '10k', 'VBUS_F', 'PSU_SENSE', 40, 22.5), r('R4', '15k', 'PSU_SENSE', 'GND', 40, 26.5),
            cp('C1', '1000u/16V', '5V', 'GND', 73, 12, fp=CP1000),
            ('U2', 'Regulator_Linear', 'LD1117V33', 'LD1117V33', 'Package_TO_SOT_THT:TO-220-3_Vertical',
             {'3': '5V', '2': '3V3', '1': 'GND'}, dict(x=73, y=22, rot=0)),
            c('C6', '100n', '5V', 'GND', 55, 26.5), cp('C11', '10u', '3V3', 'GND', 83, 12, fp=CP10),
            c('C7', '100n', '3V3', 'GND', 83, 18),
            tp('TP1', '5V', 65, 4), tp('TP2', '3V3', 68, 4), tp('TP3', 'GND', 71, 4),
        ]),
        ('MCU: ESP32-S3-DevKitC-1 gesteckt, USB-Ende zur Rueckwand, Antenne nach vorn ueber Kupfer-Sperrzone; DevKit-3V3 bleibt frei; 35-37 PSRAM, 19/20 USB, 43/44 UART0 frei, 0/3/45/46 Strapping', [
            ('U1', 'deskmate', 'ESP32-S3-DevKitC-1', 'ESP32-S3-DevKitC-1 (N16R8/N8R8)', 'deskmate:ESP32-S3-DevKitC-1_Socket',
             devkit_nets(), dict(x=18, y=42, rot=180)),
            ('J8', 'Connector_Generic', 'Conn_02x02_Odd_Even', 'RST/BOOT extern',
             'Connector_PinHeader_2.54mm:PinHeader_2x02_P2.54mm_Vertical',
             {'1': 'RST_N', '2': 'GND', '3': 'BOOT_N', '4': 'GND'}, dict(x=40, y=63, rot=0)),
            r('R6', '4k7', 'I2C_SDA', '3V3', 40, 34), r('R7', '4k7', 'I2C_SCL', '3V3', 40, 38),
            r('R8', '10k', 'IO_INT', '3V3', 40, 42),
        ]),
        ('Motor: 2x DRV8833 (PWM+DIR), VM = 5V (JP1 Default) oder MT3608-Boost an U5; nSLEEP fest an 3V3', [
            ('U3', 'deskmate', 'DRV8833_Breakout', 'DRV8833 Pololu #2130', 'deskmate:DRV8833_Socket',
             drv_nets('FADER1_PWM', 'FADER1_DIR', 'FADER2_PWM', 'FADER2_DIR', ('MOT1A', 'MOT1B'), ('MOT2A', 'MOT2B')),
             dict(x=53, y=45, rot=0)),
            ('U4', 'deskmate', 'DRV8833_Breakout', 'DRV8833 Pololu #2130 (Fader 3/4)', 'deskmate:DRV8833_Socket',
             drv_nets('FADER3_PWM', 'FADER3_DIR', 'FADER4_PWM', 'FADER4_DIR', ('MOT3A', 'MOT3B'), ('MOT4A', 'MOT4B')),
             dict(x=69, y=45, rot=0)),
            cp('C2', '100u', 'VM', 'GND', 53, 60), cp('C3', '100u', 'VM', 'GND', 69, 60),
            jp3('JP1', 'VM: 1=5V 3=Boost', '5V', 'VM', 'VBOOST', 58, 31),
            ('U5', 'deskmate', 'MT3608_Module', 'MT3608 Boost ~9V (optional, 4 Draehte)', HDR % 4,
             {'1': '5V', '2': 'GND', '3': 'VBOOST', '4': 'GND'}, dict(x=79, y=29, rot=90), True),
        ]),
        ('Peripherie: Servos + ARGB als 1x3-Stiftleisten (470u, 330R + 1000u), I2C-Leiste fuer BME680, Augen-Kabel IDC 2x5, IDC zum Frontpanel', [
            conn('J3', 3, 'Servo Pan (GND/5V/Sig)', HDR % 3, ['GND', '5V', 'SERVO_PAN'], 97, 41, 0),
            conn('J4', 3, 'Servo Tilt (GND/5V/Sig)', HDR % 3, ['GND', '5V', 'SERVO_TILT'], 97, 53, 0),
            cp('C4', '470u', '5V', 'GND', 85, 36, fp=CP470),
            conn('J5', 3, 'ARGB 5V/GND/Data', HDR % 3, ['5V', 'GND', 'WS_DATA_OUT'], 97, 65, 0),
            r('R5', '330', 'WS2812_DATA', 'WS_DATA_OUT', 89, 48, 90),
            cp('C5', '1000u', '5V', 'GND', 86, 60, fp=CP1000),
            conn('J6', 4, 'I2C / BME680 per Kabel', HDR % 4, ['3V3', 'GND', 'I2C_SCL', 'I2C_SDA'], 82, 3.6, 90),
            ('J7', 'Connector_Generic', 'Conn_02x05_Odd_Even', 'Augen-Kabel IDC 2x5', IDC10, EYE_CABLE,
             dict(x=95, y=21.5, rot=0)),
            ('J2', 'Connector_Generic', 'Conn_02x15_Odd_Even', 'IDC 2x15 -> Frontpanel', IDC, IDC_NETS,
             dict(x=52, y=95, rot=90)),
        ]),
        ('Mechanik', [hole('H1', 4, 4), hole('H2', 96, 4), hole('H3', 4, 96), hole('H4', 96, 96)]),
    ],
    'pwr_flags': ['VBUS', '5V', 'GND', 'VM', 'VBOOST'],
    'netclasses': {'Power': (['5V', 'VBUS', 'VBUS_F', 'VM', 'VBOOST', 'GND'], 1.0),
                   'Motor': (['MOT1A', 'MOT1B', 'MOT2A', 'MOT2B', 'MOT3A', 'MOT3B', 'MOT4A', 'MOT4B'], 0.6),
                   'Power3V3': (['3V3'], 0.6)},
    'keepout': [(2, 70, 34, 88)],   # unter der DevKit-Antenne (x1,y1,x2,y2): keine Kupferflaeche
    # Feste Leiterbahnen VOR dem Autorouter (Netz, Breite, Lage, Punkte)
    'pre_tracks': [('GND', 0.4, 'F.Cu', [('U1', '23'), (3.0, 68.67)]),   # Pad 23 liegt an der Antennen-Sperrzone, Flaeche kommt nicht hin
                   # 5-V-Schiene C4+ -> Servos -> ARGB -> C5+ bei x=92,5, an R5 vorbei (Freerouting fand sie mit 1 mm nicht)
                   ('5V', 1.0, 'F.Cu', [('C4', '1'), (83.25, 39.2), (92.5, 39.2), (92.5, 62.46), ('J5', '1')]),
                   ('5V', 1.0, 'F.Cu', [(92.5, 41.0), ('J3', '2')]),
                   ('5V', 1.0, 'F.Cu', [(92.5, 53.0), ('J4', '2')]),
                   ('5V', 1.0, 'F.Cu', [(92.5, 57.5), (83.5, 57.5), ('C5', '1')])],
    # Silkscreen: ('logo', x, y, Breite, Seite) · ('text', s, x, y, Groesse, Dreh, Seite, Ausr., fett) ·
    # ('pins', Ref, [Namen je Pad], dx, dy, Dreh, Ausr., Groesse) -- Name auch als (s, dx, dy, Ausr.)
    'silk': [
        ('hideref', ['J1', 'J3', 'J4', 'J5', 'J6', 'U3', 'U4', 'U5', 'TP1', 'TP2', 'TP3']),
        ('moveref', 'F1', 47.6, 15.5),
        ('logo', 54, 76, 14, 'F'),
        ('text', 'DESK-MATE', 64.5, 73.5, 3.0, 0, 'F', 'L', True),
        ('text', 'MAINBOARD · BASE', 64.5, 77.5, 1.4, 0, 'F', 'L', False),
        ('text', 'Rev 1 · 2026-10', 64.5, 80.5, 1.1, 0, 'F', 'L', False),
        ('text', 'USB-C IN 5V/3A', 40.6, 4.5, 1.2, 0, 'F', 'R', True),
        ('text', 'Kabel vom Breakout', 40.6, 7.0, 0.8, 0, 'F', 'R', False),
        ('pins', 'J1', ['VBUS', 'GND', 'CC1', 'CC2'], 0, 5.7, 0, 'C', 1.0),
        ('pins', 'TP1', ['5V'], 0, -2.3, 0, 'C', 0.8), ('pins', 'TP2', ['3V3'], 0, -2.3, 0, 'C', 0.8),
        ('pins', 'TP3', ['GND'], 0, -2.3, 0, 'C', 0.8),
        ('text', 'I2C · BME680', 82, 1.7, 0.8, 0, 'F', 'C', True),
        ('pins', 'J6', ['3V3', 'GND', 'SCL', 'SDA'], 0, 1.7, 90, 'R', 0.8),
        ('text', 'AUGEN', 89.6, 21.5, 1.2, 90, 'F', 'C', True),
        ('text', 'PAN', 97, 36.2, 1.0, 0, 'F', 'C', True), ('pins', 'J3', ['GND', '5V', 'SIG'], -1.7, 0, 0, 'R', 0.8),
        ('text', 'TILT', 97, 48.2, 1.0, 0, 'F', 'C', True), ('pins', 'J4', ['GND', '5V', 'SIG'], -1.7, 0, 0, 'R', 0.8),
        ('text', 'ARGB', 97, 60.2, 1.0, 0, 'F', 'C', True), ('pins', 'J5', ['5V', 'GND', 'DIN'], -1.7, 0, 0, 'R', 0.8),
        ('text', 'BOOST', 72.8, 29.4, 1.0, 0, 'F', 'R', True),
        ('pins', 'U5', ['IN+', 'IN-', 'OUT+', 'OUT-'], 0, -1.7, 90, 'L', 0.8),
        ('text', 'VM  1-2: 5V   2-3: BOOST', 58, 33.3, 0.8, 0, 'F', 'C', False),
        ('pins', 'J8', [('RST', -1.7, 0, 'R'), ('GND', 1.7, 0, 'L'), ('BOOT', -1.7, 0, 'R'), ('GND', 1.7, 0, 'L')], 0, 0, 0, 'C', 0.8),
        ('text', 'DRV8833 · FADER 1+2', 53, 45, 1.0, 90, 'F', 'C', False),
        ('text', 'DRV8833 · FADER 3+4', 69, 45, 1.0, 90, 'F', 'C', False),
        ('text', 'ESP32-S3-DevKitC-1', 18, 42, 1.5, 90, 'F', 'C', True),
        ('text', 'FRONTPANEL', 52, 88.9, 1.2, 0, 'F', 'C', True),
        ('logo', 18, 33, 16, 'B'),
        ('text', 'DESK-MATE', 18, 55, 3.0, 90, 'B', 'C', True),
        ('text', 'MAINBOARD · BASE · Rev 1', 63, 70, 1.2, 0, 'B', 'C', True),
        ('text', 'github.com/Kalilinuxloverr/Desk-Mate', 63, 73, 1.0, 0, 'B', 'C', False),
        ('text', 'Leon Fröhlich · 2026', 63, 75.8, 1.0, 0, 'B', 'C', False),
        ('text', 'JLCJLCJLCJLC', 63, 79, 1.0, 0, 'B', 'C', False),
    ],
}


def fader_header(n, x, y):
    return conn(f'J{13 + n}', 8, f'Fader {n} (MOT+ MOT- GND 3V3 WIPER GND TOUCH GND)', HDR % 8,
                [f'MOT{n}A', f'MOT{n}B', 'GND', '3V3', f'WIPER{n}_RAW', 'GND', f'TOUCH{n}', 'GND'], x, y, 0)


# ================================================================ FRONTPANEL 120 x 136
# Display MSP2807 (86 x 50, quer, Header links) liegt bei x 17..103, y 6..56 auf 11-mm-Abstandshaltern.
FRONT_W, FRONT_H = 120.0, 136.0
KEY_PITCH = 19.05
SOFT_Y, MACRO_Y1, MACRO_Y2 = 70.0, 96.0, 115.05
SOFT_X = [60 + (i - 2.5) * KEY_PITCH for i in range(6)]
DSP_X0, DSP_Y0 = 17.0, 6.0
FRONTPANEL = {
    'name': 'frontpanel', 'title': 'Desk-Mate Frontpanel (Deck)', 'w': FRONT_W, 'h': FRONT_H,
    'sections': [
        ('IDC vom Mainboard (Belegung Spec 2.4)', [
            ('J9', 'Connector_Generic', 'Conn_02x15_Odd_Even', 'IDC 2x15 <- Mainboard', IDC, IDC_NETS,
             dict(x=60, y=130, rot=90)),
        ]),
        ('MCP23017 (0x20): Tasten 1-10 gegen GND (interne Pull-ups), Encoder, DISP_RST (10k Pull-up, geht ueber IDC 29 auch zu den Augen), Backlight-Enable; INTA direkt an IO_INT', [
            ('U8', 'Interface_Expansion', 'MCP23017x-x-SP', 'MCP23017-E/SP', 'Package_DIP:DIP-28_W7.62mm_Socket',
             {'1': 'KEY9', '2': 'KEY10', '3': 'ENC_A', '4': 'ENC_B', '5': 'ENC_SW', '6': 'DISP_RST', '7': 'BL_EN_MCP',
              '8': None, '9': '3V3', '10': 'GND', '11': None, '12': 'I2C_SCL', '13': 'I2C_SDA', '14': None,
              '15': 'GND', '16': 'GND', '17': 'GND', '18': '3V3', '19': None, '20': 'IO_INT',
              '21': 'KEY1', '22': 'KEY2', '23': 'KEY3', '24': 'KEY4', '25': 'KEY5', '26': 'KEY6', '27': 'KEY7',
              '28': 'KEY8'}, dict(x=18, y=100, rot=0)),
            c('C12', '100n', '3V3', 'GND', 18, 79),
            r('R17', '10k', 'DISP_RST', '3V3', 18, 121.5),
        ] + [('SW%d' % (i + 1), 'Switch', 'SW_Push', 'Soft-Key %d' % (i + 1),
              'Button_Switch_Keyboard:SW_Cherry_MX_1.00u_PCB', {'1': 'KEY%d' % (i + 1), '2': 'GND'},
              dict(x=SOFT_X[i], y=SOFT_Y, rot=0)) for i in range(6)]
          + [('SW7', 'Switch', 'SW_Push', 'Makro 1', 'Button_Switch_Keyboard:SW_Cherry_MX_1.00u_PCB',
              {'1': 'KEY7', '2': 'GND'}, dict(x=SOFT_X[2], y=MACRO_Y1, rot=0)),
             ('SW8', 'Switch', 'SW_Push', 'Makro 2', 'Button_Switch_Keyboard:SW_Cherry_MX_1.00u_PCB',
              {'1': 'KEY8', '2': 'GND'}, dict(x=SOFT_X[3], y=MACRO_Y1, rot=0)),
             ('SW9', 'Switch', 'SW_Push', 'Makro 3', 'Button_Switch_Keyboard:SW_Cherry_MX_1.00u_PCB',
              {'1': 'KEY9', '2': 'GND'}, dict(x=SOFT_X[2], y=MACRO_Y2, rot=0)),
             ('SW10', 'Switch', 'SW_Push', 'Makro 4', 'Button_Switch_Keyboard:SW_Cherry_MX_1.00u_PCB',
              {'1': 'KEY10', '2': 'GND'}, dict(x=SOFT_X[3], y=MACRO_Y2, rot=0)),
             ('ENC1', 'Device', 'RotaryEncoder_Switch', 'EC11 mit Taster',
              'Rotary_Encoder:RotaryEncoder_Alps_EC11E-Switch_Vertical_H20mm',
              {'A': 'ENC_A', 'B': 'ENC_B', 'C': 'GND', 'S1': 'ENC_SW', 'S2': 'GND'}, dict(x=100, y=108, rot=0)),
             c('C13', '10n', 'ENC_A', 'GND', 95, 128), c('C14', '10n', 'ENC_B', 'GND', 105, 128)]),
        ('Bauch-Display ILI9341 2.8in SPI (MSP2807, 14-Pin, Header links); Backlight 150 mA: High-Side BC327 direkt vom MCP GPB6 (low = an); 10k B-E haelt aus, bis der MCP konfiguriert ist', [
            conn('DSP1', 14, 'ILI9341 2.8in SPI', SOCK % 14,
                 ['3V3', 'GND', 'CS_BELLY', 'DISP_RST', 'SPI_DC', 'SPI_MOSI', 'SPI_SCK', 'BELLY_BL', None, None, None,
                  None, None, None], DSP_X0 + 2.0, DSP_Y0 + 8.49 + 16.51, 0),
            ('Q1', 'Transistor_BJT', 'BC327', 'BC327', 'Package_TO_SOT_THT:TO-92_Inline',
             {'1': 'BELLY_BL', '2': 'BL_BASE', '3': '3V3'}, dict(x=40, y=30, rot=0)),
            r('R11', '1k', 'BL_EN_MCP', 'BL_BASE', 68, 20), r('R10', '10k', 'BL_BASE', '3V3', 82, 20),
        ]),
        ('Fader X32 (panel-mount, Draehte an Stiftleisten): Motor auf IDC, Schleifer ueber RC 1k/100n, Touch ueber J18 zum MPR121 (Modul per Kabel, kein Sockel: Clone-Raster unbelegt, Falle 15)', [
            fader_header(1, 6, 90), fader_header(2, 114, 88), fader_header(3, 6, 112), fader_header(4, 114, 110),
            r('R13', '1k', 'WIPER1_RAW', 'FADER1_WIPER', 9, 30, 90), c('C15', '100n', 'FADER1_WIPER', 'GND', 9, 42),
            r('R14', '1k', 'WIPER2_RAW', 'FADER2_WIPER', 111, 30, 90), c('C16', '100n', 'FADER2_WIPER', 'GND', 111, 42),
            r('R15', '1k', 'WIPER3_RAW', 'FADER3_WIPER', 9, 51, 90), c('C17', '100n', 'FADER3_WIPER', 'GND', 9, 60),
            r('R16', '1k', 'WIPER4_RAW', 'FADER4_WIPER', 111, 51, 90), c('C18', '100n', 'FADER4_WIPER', 'GND', 111, 60),
            conn('J18', 9, 'MPR121 per Kabel (ADDR am Modul an GND)', HDR % 9,
                 ['3V3', 'GND', 'I2C_SCL', 'I2C_SDA', 'IO_INT', 'TOUCH1', 'TOUCH2', 'TOUCH3', 'TOUCH4'], 92, 88, 90),
        ]),
        ('Mechanik: 4 Ecken + 4 Display-Abstandshalter (M3 x 11 mm, Raster 76,08 x 44)', [
            hole('H5', 4, 4), hole('H6', 116, 4), hole('H7', 4, 132), hole('H8', 116, 132),
            hole('H9', DSP_X0 + 4.96, DSP_Y0 + 3.0), hole('H10', DSP_X0 + 81.04, DSP_Y0 + 3.0),
            hole('H11', DSP_X0 + 4.96, DSP_Y0 + 47.0), hole('H12', DSP_X0 + 81.04, DSP_Y0 + 47.0)]),
    ],
    'pwr_flags': ['5V', '3V3', 'GND'],
    'netclasses': {'Power': (['5V', 'GND'], 0.8), 'Power3V3': (['3V3', 'BELLY_BL'], 0.6),
                   'Motor': (['MOT1A', 'MOT1B', 'MOT2A', 'MOT2B', 'MOT3A', 'MOT3B', 'MOT4A', 'MOT4B'], 0.6)},
    'keepout': [],
    'silk': [
        ('hideref', ['J9', 'J14', 'J15', 'J16', 'J17']),
        ('logo', 58, 38, 20, 'F'),
        ('text', 'DESK-MATE', 73, 35.5, 3.5, 0, 'F', 'L', True),
        ('text', 'FRONTPANEL · DECK', 73, 40.5, 1.5, 0, 'F', 'L', False),
        ('text', 'Rev 1 · 2026-10', 73, 43.5, 1.1, 0, 'F', 'L', False),
        ('logo', 92, 121.5, 9, 'F'),
        ('text', 'DESK-MATE', 98.5, 121.3, 1.6, 0, 'F', 'L', True),
        ('text', 'Frontpanel Rev 1', 98.5, 123.9, 0.9, 0, 'F', 'L', False),
        ('text', 'DISPLAY 2,8 ZOLL', 21.6, 31, 1.0, 90, 'F', 'C', True),
        ('pins', 'DSP1', ['VCC', 'GND', 'CS', 'RST', 'DC', 'SDI', 'SCK', 'LED', 'SDO', 'T_CLK', 'T_CS', 'T_DIN', 'T_DO', 'T_IRQ'],
         -1.7, 0, 0, 'R', 0.8),
        ('text', 'FADER 1', 2.6, 90, 1.0, 90, 'F', 'C', True),
        ('text', 'FADER 3', 2.6, 112, 1.0, 90, 'F', 'C', True),
        ('text', 'FADER 2', 117.4, 88, 1.0, 90, 'F', 'C', True),
        ('text', 'FADER 4', 117.4, 110, 1.0, 90, 'F', 'C', True),
    ] + [('pins', f'J{r}', ['M+', 'M-', 'GND', '3V3', 'WIP', 'GND', 'TCH', 'GND'], dx, 0, 0, j, 0.8)
         for r, dx, j in ((14, 1.7, 'L'), (16, 1.7, 'L'), (15, -1.7, 'R'), (17, -1.7, 'R'))] + [
        ('text', 'MPR121', 92, 85.6, 1.0, 0, 'F', 'C', True),
        ('pins', 'J18', ['3V3', 'GND', 'SCL', 'SDA', 'IRQ', 'T1', 'T2', 'T3', 'T4'], 0, 1.7, 90, 'R', 0.8),
        ('text', 'MAINBOARD', 35.5, 131, 1.2, 0, 'F', 'R', True),
        ('logo', 60, 36, 22, 'B'),
        ('text', 'DESK-MATE · FRONTPANEL · Rev 1', 60, 47.8, 1.2, 0, 'B', 'C', True),
        ('text', 'github.com/Kalilinuxloverr/Desk-Mate', 60, 50.4, 1.0, 0, 'B', 'C', False),
        ('text', 'Leon Fröhlich · 2026', 60, 52.8, 1.0, 0, 'B', 'C', False),
        ('text', 'JLCJLCJLCJLC', 60, 55.2, 1.0, 0, 'B', 'C', False),
    ],
}

# ================================================================ AUGEN-ADAPTER 42 x 30
EYE_W, EYE_H = 42.0, 30.0
EYEADAPTER = {
    'name': 'eye-adapter', 'title': 'Desk-Mate Augen-Adapter (Kopf)', 'w': EYE_W, 'h': EYE_H,
    'sections': [
        ('Nur Stecker: IDC 2x5 vom Mainboard -> 2x 1x7-Stiftleiste in GC9A01-Reihenfolge (VCC GND SCL SDA RES DC CS), Displays per Dupont-Kabel; DISP_RST kommt vom MCP23017', [
            ('J11', 'Connector_Generic', 'Conn_02x05_Odd_Even', 'IDC 2x5 vom Mainboard J7', IDC10, EYE_CABLE,
             dict(x=21, y=8, rot=90)),
            conn('J12', 7, 'GC9A01 links (Dupont)', HDR % 7, ['3V3', 'GND', 'SPI_SCK', 'SPI_MOSI', 'DISP_RST', 'SPI_DC', 'CS_EYE_L'],
                 11, 24, 90),
            conn('J13', 7, 'GC9A01 rechts (Dupont)', HDR % 7, ['3V3', 'GND', 'SPI_SCK', 'SPI_MOSI', 'DISP_RST', 'SPI_DC', 'CS_EYE_R'],
                 31, 24, 90),
            c('C20', '100n', '3V3', 'GND', 14, 17.5),
            c('C21', '100n', '3V3', 'GND', 28, 17.5),
        ]),
        ('Mechanik', [hole('H13', 4, 4), hole('H14', 38, 4)]),
    ],
    'pwr_flags': ['3V3', 'GND'],
    'netclasses': {'Power3V3': (['3V3', 'GND'], 0.6)},
    'keepout': [],
    'silk': [
        ('logo', 36.5, 12.5, 7, 'F'),
        ('text', 'AUGEN', 5.5, 10.5, 1.2, 0, 'F', 'C', True),
        ('text', 'Rev 1', 5.5, 13, 0.9, 0, 'F', 'C', False),
        ('text', 'MAINBOARD', 21, 1.7, 0.8, 0, 'F', 'C', True),
        ('text', 'AUGE L', 6, 20.8, 0.9, 0, 'F', 'C', True),
        ('text', 'AUGE R', 36, 20.8, 0.9, 0, 'F', 'C', True),
        ('pins', 'J12', ['VCC', 'GND', 'SCL', 'SDA', 'RES', 'DC', 'CS'], 0, 1.7, 90, 'R', 0.8),
        ('pins', 'J13', ['VCC', 'GND', 'SCL', 'SDA', 'RES', 'DC', 'CS'], 0, 1.7, 90, 'R', 0.8),
        ('logo', 5.5, 12, 7, 'B'),
        ('text', 'github.com/Kalilinuxloverr/Desk-Mate', 21, 20.5, 0.8, 0, 'B', 'C', False),
        ('text', 'JLCJLCJLCJLC', 36.6, 12, 0.8, 0, 'B', 'C', False),
    ],
}

BOARDS = [MAINBOARD, FRONTPANEL, EYEADAPTER]
