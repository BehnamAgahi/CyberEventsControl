import json

from types import SimpleNamespace

with open('channels_messages.json', 'r') as filehandle:

    messagesList = json.load(filehandle)

i = 0

while i < len(messagesList):

    stringIterator = json.dumps(messagesList[i])

    messagesList[i] = json.loads(stringIterator, object_hook = lambda d: SimpleNamespace(**d))

    i = i + 1

companiesNames = []

with open("companies.ini", encoding="utf8") as companiesFile:

    for line in companiesFile:

        line = line.strip()

        companiesNames.append(line)

i = 0

signals = []

while i < len(messagesList):

    if hasattr(messagesList[i], 'message'):

        for j in companiesNames:

            if j in messagesList[i].message:

                setattr(messagesList[i], 'company', j)

                signals.append(messagesList[i])

                break

    i = i + 1

buyTags = []

with open("buy.ini", encoding="utf8") as buyFile:

    for line in buyFile:

        line = line.strip()

        buyTags.append(line)

analyzedBuySignals = []

i = 0

while i < len(signals):

    if hasattr(signals[i], 'message'):

        for j in buyTags:

            if j in signals[i].message:

                setattr(signals[i], 'buy', True)

                analyzedBuySignals.append(signals[i])

                break

    i = i + 1

sellTags = []

with open("sell.ini", encoding="utf8") as sellFile:

    for line in sellFile:

        line = line.strip()

        sellTags.append(line)

analyzedSellSignals = []

i = 0

while i < len(signals):

    if hasattr(signals[i], 'message'):

        for j in sellTags:

            if j in signals[i].message:

                setattr(signals[i], 'sell', True)

                analyzedSellSignals.append(signals[i])

                break

    i = i + 1

with open('analyzedBuySignals.json', 'w') as filehandle:

    json.dump(analyzedBuySignals, filehandle,  default = lambda o: o.__dict__, 
            sort_keys = True, indent = 4)

with open('analyzedSellSignals.json', 'w') as filehandle:

    json.dump(analyzedSellSignals, filehandle, default = lambda o: o.__dict__, 
            sort_keys = True, indent = 4)

with open('signals.json', 'w') as filehandle:

    json.dump(signals, filehandle, default = lambda o: o.__dict__, 
            sort_keys = True, indent = 4)
