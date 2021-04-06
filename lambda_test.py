
import boto3
import json
import random

IMAGE_ID = 'ami-0121ef35996ede438'
InstanceType = 't3.medium'
IamInstanceProfile = 'arn:aws:iam::590100935479:role/lambdaControlEC2'
SecurityGroupId = 'sg-02ef6b6c1b6f17c12'

KEY_NAME = 'test'

VPN_EMAIL = 'samnickolay@gmail.com'
VPN_PASSWORD = 'z3NjbYH8stYFZEi'

PLAYLISTS = ['spotify:playlist:5PkrnGrf4RN2UtHCad45Yu', 'spotify:playlist:5PkrnGrf4RN2UtHCad45Yu',
             'spotify:playlist:2N5MFM7E8OXrj5JEiRDRL3', 'spotify:playlist:2N5MFM7E8OXrj5JEiRDRL3',
             'spotify:playlist:37i9dQZF1DXcBWIGoYBM5M']
PLAYLIST = random.choice(PLAYLISTS)

print(PLAYLIST)

region = 'us-west-1'

accounts = {
    'samnickolay@gmail.com': 'Tlbsj5116',
    'harperyoung@vizy.io': '9RSA769PNb56!?',
    'genetaylor@vizy.io': '5kXcFXPLxWJL!?',
    'phoenixgriffiths@vizy.io': 'wGcbApcfFyKs!?',
    'danniwood@vizy.io': 'ZNDL6FbqVfKV!?',
    'alexreid@vizy.io': 'T2x98cGUC3A8!?',
    'chrischaney@vizy.io': 'mzhAHDkEG2He!?',
}

all_accounts = {'harperyoung@vizy.io': '9RSA769PNb56!?',
                'genetaylor@vizy.io': '5kXcFXPLxWJL!?',
                'phoenixgriffiths@vizy.io': 'wGcbApcfFyKs!?',
                'danniwood@vizy.io': 'ZNDL6FbqVfKV!?',
                'alexreid@vizy.io': 'T2x98cGUC3A8!?',
                'chrischaney@vizy.io': 'mzhAHDkEG2He!?',
                'riverburton@vizy.io': 'zWQEqNEad8uh!?',
                'carmenmoran@vizy.io': 'x4S9ZxMR8qqj!?',
                'erinboone@vizy.io': 'DncBCZbMzvpF!?',
                'brynnratliff@vizy.io': 'vtVPXG4WVzKt!?',
                'skylercooke@vizy.io': 'mSM7ba9D7zuS!?',
                'judefletcher@vizy.io': 'RgvBZz6pWTvb!?',
                'drewwhite@vizy.io': 'T3PmqY6zpWqx!?',
                'jordanmatthews@vizy.io': 'uWnBcdteMdQH!?',
                'riverkaur@vizy.io': 'kFMccVuR3FjS!?',
                'harpernorris@vizy.io': 'XAycrx4BD2gc!?',
                'loganbryan@vizy.io': '9twZW4qBQMPt!?',
                'alexrose@vizy.io': 'wV3PWU7dy9sa!?',
                'rayleereed@vizy.io': '9SgUfJsAgMsZ!?',
                'riverallison@vizy.io': 'LYfrF8T2tqNG!?',
                'kaiparry@vizy.io': 'Zh2fuQLvMh5W!?',
                'aarenburton@vizy.io': '8ETUDLWp6nvW!?',
                'frankybradley@vizy.io': 'pNkMTaMgpjKu!?',
                'jessknight@vizy.io': 'rRLACcVUmmBc!?',
                'alexstone@vizy.io': 'QD4puAhj65dA!?',
                'geneschwartz@vizy.io': 'yLRPK2dYMhng!?',
                'brynncummings@vizy.io': 'pDW9bErDWKN2!?',
                'jessiefulton@vizy.io': 'utGHFFZbNtpS!?',
                'brettchang@vizy.io': 'HWvaPRnZzYfe!?',
                'erinknapp@vizy.io': '6uaBTV93qBN6!?',
                'aarenhall@vizy.io': 'RWDtuXLaSfAh!?',
                'renemason@vizy.io': 'bCRH8MDzQkwQ!?',
                'riversaunders@vizy.io': '8LpbraZr2LKQ!?',
                'dennyrichards@vizy.io': 'j8KpTcCU8S9p!?',
                'viccooke@vizy.io': '7jW233dAYsJY!?',
                'terrymcintosh@vizy.io': 'veLqZzbHhRA8!?',
                'baileyelliott@vizy.io': 'ywTN6KZdjary!?',
                'maddoxnixon@vizy.io': '6xHaFfUsdKc8!?',
                'leighcarey@vizy.io': '36t9An3aPRTH!?',
                'caseymacias@vizy.io': 'DU7gEgxQQQ8G!?',
                'judegreen@vizy.io': 'NNtxdGLRHFJu!?',
                'jordanbrooks@vizy.io': 'bma2Mw4JNdSD!?',
                'quinnwoods@vizy.io': 'CEAV4qjuRBKx!?',
                'angelhunt@vizy.io': 'eeARBFr8rc4B!?',
                'lanelee@vizy.io': 'mARRPbT4wJDM!?',
                'corycarney@vizy.io': 'd9SbeAYa6y2n!?',
                'loganbean@vizy.io': 'jr2kpHCSPEtA!?',
                'gabbyandrews@vizy.io': '3MDGum5H469A!?',
                'kaiwest@vizy.io': 'LMm4HCszV54c!?',
                'dannyhamilton@vizy.io': 'dBKzqKnGLsrm!?',
                'gabbymarshall@vizy.io': 'G2ydmPBfCT7v!?',
                'generichardson@vizy.io': 'jxFsQWmUWZWX!?',
                'reedaustin@vizy.io': '4n9HtmPwz4XJ!?',
                'briceharper@vizy.io': 'HJLxSA8Z9fcj!?',
                'cameronwalsh@vizy.io': 'R5kL9DFrTjBx!?',
                'jofigueroa@vizy.io': 'VF7RPWCQKPNv!?',
                'gabegilmore@vizy.io': 'EERWcR7K4ahG!?',
                'sidneybradford@vizy.io': 'GjYpNMyBKxcv!?',
                'jackieleblanc@vizy.io': 'bppDJ23kGsWa!?',
                'charliechurch@vizy.io': 'AfegHc4Lr6Rr!?',
                'clemsimpson@vizy.io': '4Dwgb5AWVhCQ!?',
                'blairmills@vizy.io': 'yevAFTE9eXRK!?',
                'billieparry@vizy.io': 'ZJKqK7ykWpcY!?',
                'dannyprice@vizy.io': '8khcP2qsMWLp!?',
                'aidensmith@vizy.io': 'tcaFaA567bd6!?',
                'cameroncraft@vizy.io': 'nDqzbUBjWuC9!?',
                'blaketaylor@vizy.io': 'VbtgfLk2QqAe!?',
                'franbrown@vizy.io': 'N2Q4Tsfktww3!?',
                'glennleonard@vizy.io': 'grqu6N7waH65!?',
                'baileyanthony@vizy.io': 'EmWetLdm5k7Y!?',
                'drewrobertson@vizy.io': 'D8z8PPBASjkj!?',
                'ashleyblack@vizy.io': '2MnNF8wWMbAg!?',
                'sammyscott@vizy.io': 'XnWGuD8DuYkm!?',
                'quinnharper@vizy.io': 'HDquqCQmJ6a5!?',
                'lesleylloyd@vizy.io': '6CShev6pT5AQ!?',
                'sidneybean@vizy.io': 'kfAjA45nLfJL!?',
                'riverlane@vizy.io': 'qDtpXBSVTEdf!?',
                'rayleesargent@vizy.io': 'ZgEyFTm2Hfjm!?',
                'alexguerrero@vizy.io': 'F2MqXDM6MnAS!?',
                'jamiebonner@vizy.io': 'nbrcPsLdPdR9!?',
                'quinnmarshall@vizy.io': 'yXyuG4KEWFF8!?',
                'gailelliott@vizy.io': 'cXUd3nb9LAGg!?',
                'sammurray@vizy.io': 'XE6JuVhUzRvv!?',
                'kitberry@vizy.io': 'QhWVQRJrjtzv!?',
                'charliehayes@vizy.io': 'Zjkx9EFMntSk!?',
                'noelmaldonado@vizy.io': 'ZMdyJ5PpDenT!?',
                'samspence@vizy.io': '3qcRmbMYBgMh!?',
                'aarenpotter@vizy.io': '2bkeghAqvMkR!?',
                'rudylamb@vizy.io': 'PpxmmnLSBXFr!?',
                'renestanley@vizy.io': 'rZZ6DgG7nGkm!?',
                'alimacdonald@vizy.io': '9GzpQZXSRLMJ!?',
                'kaibaxter@vizy.io': 'x3gsATnCCaHu!?',
                'kaibarrett@vizy.io': '3WrvXK8wgbEx!?',
                'judeblack@vizy.io': 'GwTeftLZGMmv!?',
                'jackiejohnston@vizy.io': 'jdjh6Fw8CmtZ!?',
                'aarensellers@vizy.io': '5kP7eSJV9L6u!?',
                'drewgarrett@vizy.io': 'uyXQytZEhJBc!?',
                'reggieharmon@vizy.io': 'MRKgDLFnKp5N!?',
                'bretlogan@vizy.io': 'aCx9gZPZ2w5B!?',
                'jaimehyde@vizy.io': 'YuBCnjsLw48V!?',
                'samtaylor@vizy.io': 'aRHBuM7kURBY!?',
                'jadenfoster@vizy.io': 'k74hTUm8x2gb!?',
                'jodynicholson@vizy.io': '8PrwXRQmhn4x!?',
                'frankyryan@vizy.io': 'yKyz4KXsLdJf!?',
                'brookcook@vizy.io': 'gav5tcX6zGzx!?',
                'dannyclarke@vizy.io': 'F9nDLZjKyrMW!?',
                'aarenbush@vizy.io': 'qCZrRsxkLwVX!?',
                'jodyashley@vizy.io': 'pV77gCdtTsEU!?',
                'alexishicks@vizy.io': '2ysSrNfdnDXw!?',
                'carmenferguson@vizy.io': 'qErkKzzm62Uh!?',
                'elipoole@vizy.io': 'sbLXRJZAAv9c!?',
                'gabbycooke@vizy.io': 'KpGW5NTSBrB8!?',
                'lesliejones@vizy.io': 'ehrqnjAns7nj!?',
                'bevrobinson@vizy.io': 'UMLpqCMwV583!?',
                'taylorhawkins@vizy.io': 'Vc63CxzGw9pU!?',
                'blairbarr@vizy.io': 'QD7awT59jkhf!?',
                'leepayne@vizy.io': 'ayZ8KtX8Egcf!?',
                'drewstark@vizy.io': 'BmGGRYJ4uAqk!?',
                'jodyfinley@vizy.io': 'DZsZ52yVxR7D!?',
                'renetyson@vizy.io': '7jQyKRTjaCS3!?',
                'rudyelliott@vizy.io': 'r2AzBpnWz6by!?',
                'cameronduncan@vizy.io': 'SvmcLCpz7uBw!?',
                'emersonphillips@vizy.io': 'puKCW6KBb3At!?',
                'nickygordon@vizy.io': '83kSXPMMRa9E!?',
                'emersonmoore@vizy.io': 'EHubEvKcFsm5!?',
                'rowanshaw@vizy.io': 'Nsjduyhy4kQR!?',
                'aidenhuber@vizy.io': 'ez7z4RfHL4nc!?',
                'krisstephenson@vizy.io': 'FghvbKbbr3Sg!?',
                'genedelaney@vizy.io': 'S5sKbPhpGCMK!?',
                'aidenkirkland@vizy.io': '6c9zTW2Rczr2!?',
                'morganprice@vizy.io': 'ZcQYN2ga8hwB!?',
                'harleylowe@vizy.io': 'WcvPjZGJdjZU!?',
                'jadenday@vizy.io': 'pgURHqMC3paS!?',
                'rayhussain@vizy.io': 'vP9wGvqUsT6t!?',
                'marleyadams@vizy.io': 'FFUWCvZJjWaK!?',
                'kitsosa@vizy.io': '4AmNuhpzjWWE!?',
                'frankieowen@vizy.io': 'KMRPQy6mjMXc!?',
                'angelmadden@vizy.io': 'VQ39fvDfkhuK!?',
                'glennholland@vizy.io': 'WLLDmdKA42Pn!?',
                'clembarker@vizy.io': 'zN8cKFBe6GzP!?',
                'averywilliams@vizy.io': 'qWgZBtvKFBjN!?',
                'sidneygrant@vizy.io': '95VGA4ZuNkkG!?',
                'willyholland@vizy.io': 'EphkrU2YejdJ!?',
                'cameronlee@vizy.io': 'uwLZpM97Cxcq!?',
                'rorysutton@vizy.io': 'BEZhf7ZN7vZU!?',
                'charliehensley@vizy.io': 'vudsdqvvMXXs!?',
                'mellbaxter@vizy.io': 'e8HvJrXKeNbY!?',
                'marleyhicks@vizy.io': 'NK4haqnBnDjk!?',
                'frankieschultz@vizy.io': 'hqwTfcaph8nU!?',
                'rayleebooth@vizy.io': 'mndksDtbhJYn!?',
                'brethunt@vizy.io': 'nqZVAhsQkCqR!?',
                'jesseroberts@vizy.io': 'EvRsRwyvALYc!?',
                'ashleychambers@vizy.io': 'S9VsPudQMWeN!?',
                'gailwilson@vizy.io': 'ZXE3FWV7UU38!?',
                'bricejordan@vizy.io': 'kT4w99FZLPNr!?',
                'shaygillespie@vizy.io': 'QA4DgCAEHufE!?',
                'haydenduffy@vizy.io': 'RqcabVr622mA!?',
                'rivermccarty@vizy.io': 'RThVyZJZScjX!?',
                'corystein@vizy.io': 'z6k6GV9BNB9z!?',
                'jodybattle@vizy.io': 'nT64Ee8fGqZk!?',
                'reneatkinson@vizy.io': 'c2XBwuYjnUau!?',
                'franbarker@vizy.io': 'tdcv4GHcfyJE!?',
                'roryward@vizy.io': 'GdN5TsKMBU77!?',
                'phoenixwells@vizy.io': 'TH7bc9r7yh48!?',
                'jackielewis@vizy.io': 'WU4wScDznszh!?',
                'willyconway@vizy.io': 'Wkd4fSnFNf9f!?',
                'renestrong@vizy.io': 'Jf4SE67hbzDu!?',
                'averyhodges@vizy.io': '8yJ3xu3xvcga!?',
                'ashleyhall@vizy.io': 'jaQ4Hb9KVXt6!?',
                'robintravis@vizy.io': 'SNKQTwEuHgYq!?',
                'valellis@vizy.io': 'D894c23AGTFu!?',
                'blakewatts@vizy.io': 'bQDrmCZ9xb3G!?',
                'leesharp@vizy.io': 'KqVW8uE7TXCT!?',
                'nickymartin@vizy.io': 'AYjcWVgsjSM8!?',
                'haydenjordan@vizy.io': 'BDjKADRRFhJx!?',
                'jamiemarks@vizy.io': 'WEW5uwcMHnEM!?',
                'leighchan@vizy.io': 'EDhC4ZF7kgwT!?',
                'jackiemcintosh@vizy.io': '6VRkHz79GmNu!?',
                'carmenconrad@vizy.io': 'phuQHj6KNk2t!?',
                'robinhutchinson@vizy.io': 'b24PLpEKmEnM!?',
                'krislawrence@vizy.io': 'SteqybD6Etmk!?',
                'clemmurphy@vizy.io': 'YKx5dTgc7U5z!?',
                'alexiswalker@vizy.io': 'ruB7R8fbGe3R!?',
                'addisonlawrence@vizy.io': '9Cf6jLGwN3VX!?',
                'krisknight@vizy.io': 'rUX7kru9npzt!?',
                'haydenmanning@vizy.io': 'JAW5qEU9GFE7!?',
                'emersonrichmond@vizy.io': '5z7xgMMHZHFy!?',
                'clemsharp@vizy.io': 'sXcVMwNFRh82!?',
                'billysargent@vizy.io': 'DQgy4WgsvjWe!?',
                'caseygallagher@vizy.io': 'cwsNuaqqgM5c!?',
                'rudyjames@vizy.io': 'jpxZQq6hpGzP!?',
                'noelsutton@vizy.io': 'nZyrpg6vsfnz!?',
                'ashtongibson@vizy.io': 'SKu9ZfhLrNn6!?',
                'raymatthews@vizy.io': 'RMfgGxfKVmA6!?',
                'krisduncan@vizy.io': 'k4ZxEAcjYHgr!?',
                'frankiepope@vizy.io': 'TMPhKpeHsvvV!?',
                'aarenfranks@vizy.io': 'X24UGBT3bTnY!?',
                'willwitt@vizy.io': '2UJ9KCfxgAx7!?',
                'dannipennington@vizy.io': 'XcTaCzJ2Qm7E!?',
                'silvermaxwell@vizy.io': '5c266P7mxPPk!?',
                'carolburke@vizy.io': '9sKQ9A3wJPth!?',
                'angelgordon@vizy.io': 'BLSS3r82UKr9!?',
                'willrichards@vizy.io': 'HcsBsjwLnSjz!?',
                'dennydoyle@vizy.io': 'hKLNeggN3J4H!?',
                'jadenjohnson@vizy.io': '7hfbbjaLkw5X!?',
                'jackiepeck@vizy.io': 'YAtpUKgjm3af!?',
                'harpervinson@vizy.io': 'Ws4aqGyELwvz!?',
                'drewwalton@vizy.io': 'a3aspNPZTy9g!?',
                'caseycarver@vizy.io': 'GZWyykxAb5vk!?',
                'rivercotton@vizy.io': 'd5mESbGvEFnh!?',
                'taylorhussain@vizy.io': 'FLAQppPm2cGd!?',
                'skyejenkins@vizy.io': 'd7DLwGCAgArC!?',
                'aubreynewman@vizy.io': 'Rgw8hhL66FgX!?',
                'leslieburns@vizy.io': 'gKEenGJKTsHR!?',
                'rileycox@vizy.io': 'Y5fWzVjkHp4u!?',
                'willydeleon@vizy.io': '37h7B2Ujpedc!?',
                'jamieacevedo@vizy.io': 'cSMrQvDzNYtT!?',
                'charliekent@vizy.io': 'MwZLRZyty8vv!?',
                'angelneal@vizy.io': 'ZDqUqRHtmtt5!?',
                'krisbrennan@vizy.io': 'TzyuCkDePCED!?',
                'glenpalmer@vizy.io': 'pAp4Zq3eVaJF!?',
                'loganturner@vizy.io': 'M2RxzkPPpGvz!?',
                'lesliegallagher@vizy.io': 'hLEf6Qsecw42!?',
                'riverlawrence@vizy.io': 'GXWfUvB9WFCt!?',
                'valstevens@vizy.io': '824PV2Lmha7X!?',
                'brooksykes@vizy.io': 'FDYGTKedYcRb!?',
                'marleymoreno@vizy.io': 'hTF2SMzj6XtP!?',
                'jackiebishop@vizy.io': 'AB5aV9gjw7HE!?',
                'billieblackwell@vizy.io': 'wRqz8uMqSB9C!?',
                'ashtonweiss@vizy.io': '3YJKG4F334A7!?',
                'aliphillips@vizy.io': 'Q59Z3r5xUpU2!?',
                'skylarwatts@vizy.io': 'QW6xVD5uJdPJ!?',
                'mellandrews@vizy.io': '8pCJRdcZQKQ5!?',
                'morganwells@vizy.io': 'DjRxxugynxJn!?',
                'emersonhussain@vizy.io': 'JPDSpRvw45Cd!?',
                'jessdeleon@vizy.io': 'VWGpKEg3TGBb!?',
                'leslielamb@vizy.io': '3usN98JvDHNG!?',
                'ashtonrasmussen@vizy.io': 'XhCZ3pnd25yq!?',
                'alexmartin@vizy.io': '8Ng3KSGUNWYv!?',
                'reggiejensen@vizy.io': 'aLUatM3GDfBe!?',
                'bevhamilton@vizy.io': 'QsZbcrya6prg!?',
                'roryfrancis@vizy.io': 'KD78DdLYnccM!?',
                'rayhenderson@vizy.io': 'Ejksjh9wrHHz!?',
                'bretnicholson@vizy.io': 'rA9dLkpGxV4R!?',
                'joyoung@vizy.io': 'K6MgM2rxxT8E!?',
                'asholson@vizy.io': 'FerdLAdmgyKW!?',
                'frankyhenry@vizy.io': '7aDxgUjTrJed!?',
                'leighchavez@vizy.io': 'PC3UEfNfqcUc!?',
                'aarenferrell@vizy.io': 'f4vD4QUpuWg8!?',
                'mellbates@vizy.io': 'ARDHNs3xA6S7!?',
                'brookjones@vizy.io': 'fX42HEjvYEQM!?',
                'melhunter@vizy.io': 'FVrsC76R7G2s!?',
                'taylorbaxter@vizy.io': 'SK36DFbeGGhy!?',
                'erinclarke@vizy.io': 'a3jbHHcSevzj!?',
                'danebaxter@vizy.io': 'FdA26QHJE22Q!?',
                'bricehopper@vizy.io': 'dkR2usrHc6uH!?',
                'reggiesimon@vizy.io': 'DyB7GaXFPsjH!?',
                'morganbarlow@vizy.io': 'RF6zUmgrBkxe!?',
                'ashtonsnider@vizy.io': 'ckK3ggK2F6d5!?',
                'samshepherd@vizy.io': 'Gba6ktWMdwqD!?',
                'harpergray@vizy.io': 'tYhHKSVgJsdF!?',
                'glenharris@vizy.io': 'v8rJPkWGru4q!?',
                'gabbythompson@vizy.io': 'ttfsqG6XF5r7!?',
                'erinmacdonald@vizy.io': 'MYxu6t47TLaa!?',
                'alexishopkins@vizy.io': 'LR4m5wFf7E7W!?',
                'charliehenson@vizy.io': '8gkn8CdRfvBT!?',
                'danninieves@vizy.io': 'wbVTdxKaMwEs!?',
                'krisjustice@vizy.io': 'maSyCr3hbc4w!?',
                'jessewolf@vizy.io': '6gU8x67ED9Gm!?',
                'elliotreese@vizy.io': 'H7Bk7gAdZphY!?',
                'coryparry@vizy.io': 'Qyjweva9HecU!?',
                'reggieberry@vizy.io': 'wMtFEszgd23M!?',
                'dennyedwards@vizy.io': 'kp8JhmEgUn75!?',
                'aarencole@vizy.io': 'x5GweA2KkQ3H!?',
                'billiepatel@vizy.io': 'jdvG5MHw95d3!?',
                'haydenmack@vizy.io': 'MX4SPtFYTypW!?',
                'blaircleveland@vizy.io': 'ASVFfqZHSW28!?',
                'brettconway@vizy.io': '97QeHJn6SZZe!?',
                'bevmanning@vizy.io': 'Njczu9mfFYEY!?',
                'elichambers@vizy.io': 'EeyFyPZ4eZp5!?',
                'dennyjackson@vizy.io': 'Q8AT9xm4YDHx!?',
                'coryryan@vizy.io': 'ShwXfgkkV2RT!?',
                'alexisarmstrong@vizy.io': 'PJUTAjjp4wWa!?',
                'jordankelly@vizy.io': 'v3CtPhkX7rAZ!?',
                'gabenicholson@vizy.io': 'j3asRzSeUM8K!?',
                'aarenparrish@vizy.io': '5WUKPmkxXTTB!?',
                'willbaird@vizy.io': 't4Sxrz5L8USx!?',
                'krisfulton@vizy.io': 'uYSnfgQRWVTM!?',
                'jaimerich@vizy.io': 'QExQQ4Gp5kvM!?',
                'haydendecker@vizy.io': 'f5aEacSE8bqX!?',
                'skylarmarsh@vizy.io': 'SvqzEFKb9MQX!?',
                'ashtonroberts@vizy.io': 'g864X38SNjZS!?',
                'bricebarnes@vizy.io': 'zP5emVjqseen!?',
                'caseyanderson@vizy.io': 'LBKX3KyZbkXy!?',
                'kiranbates@vizy.io': 'GpxMWHNEPGsk!?',
                'gailadams@vizy.io': 'xSvt4jzZ9S3T!?',
                'aarenhenry@vizy.io': 'm3vnsduLJXGe!?',
                'tylergutierrez@vizy.io': '3uTTeqdqZ6bB!?',
                'dennyhayes@vizy.io': 'xqpzvgy3grar!?',
                'caseylara@vizy.io': 'bdhFazFG245X!?'

                }


user_data = '''#!/bin/bash -xe
# exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1
echo "fetching bash script"
wget -N https://raw.githubusercontent.com/samnickolay/spotify-test12345/main/public_script.sh
chmod +x ./public_script.sh
echo "running bash script"
# ./public_script.sh 2>/home/ubuntu/stderr.log 1>/home/ubuntu/stdout.log
./public_script.sh 2>&1 | tee /home/ubuntu/stdout.log

'''

ec2 = boto3.client('ec2', region_name=region)
iam = boto3.client('iam', region_name=region)


def lambda_handler(event, context):
    print('lambda_handler starting')

    reservations = ec2.describe_instances(Filters=[{"Name": "instance-state-name", "Values": ["running"]}]).get("Reservations")

    instance_ids = []
    for reservation in reservations:
        for instance in reservation["Instances"]:
            print(instance['InstanceId'] + ' - ' + instance['ImageId'])
            if instance['ImageId'] == IMAGE_ID:
                instance_ids.append(instance['InstanceId'])
    try:
        result = ec2.terminate_instances(InstanceIds=instance_ids)
        print(result)
    except Exception as _e:
        print(_e)

    for email, password in accounts.items():
        TAG_SPEC = [
            {
                "ResourceType": "instance",
                "Tags": [
                    {
                        "Key": "vpn_email",
                        "Value": VPN_EMAIL,
                    },
                    {
                        "Key": "vpn_password",
                        "Value": VPN_PASSWORD,
                    },
                    {
                        "Key": "playlist",
                        "Value": PLAYLIST,
                    },
                    {
                        "Key": "spotify_email",
                        "Value": email,
                    },
                    {
                        "Key": "spotify_password",
                        "Value": password,
                    }
                ]
            }
        ]

        print(TAG_SPEC)

        # instance_profile = iam.create_instance_profile(InstanceProfileName='Test-instance-profile2')
        # print(instance_profile)
        # response = iam.add_role_to_instance_profile(InstanceProfileName='Test-instance-profile2', RoleName='ec2ReadTags')
        # print(response)

        launchedInstances = ec2.run_instances(
            MaxCount=1,
            MinCount=1,
            ImageId=IMAGE_ID,
            InstanceType=InstanceType,
            IamInstanceProfile={'Name': 'Test-instance-profile2'},
            SecurityGroupIds=[SecurityGroupId],
            TagSpecifications=TAG_SPEC,
            UserData=user_data,
            KeyName=KEY_NAME
        )

        print(launchedInstances)

    print('lambda_handler finishing')

    return {
        'statusCode': 200,
        'body': json.dumps(PLAYLIST)
    }
