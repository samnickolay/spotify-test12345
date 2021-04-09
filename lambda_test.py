
import boto3
import json
import random

IMAGE_ID = 'ami-0121ef35996ede438'
InstanceType = 't3.medium'
IamInstanceProfile = 'arn:aws:iam::590100935479:role/lambdaControlEC2'
SecurityGroupId = 'sg-02ef6b6c1b6f17c12'

KEY_NAME = 'test'

# VPN_EMAIL = 'samnickolay@gmail.com'
# VPN_PASSWORD = 'z3NjbYH8stYFZEi'

vpn_accounts = {
    # 'samnickolay@gmail.com': 'z3NjbYH8stYFZEi',
    'nordvpn1@vizy.io': '3cPDMityEM85xhq',
    'nordvpn2@vizy.io': '3cPDMityEM85xhq',
    'nordvpn3@vizy.io': '3cPDMityEM85xhq',
    'nordvpn4@vizy.io': '3cPDMityEM85xhq',
    'nordvpn5@vizy.io': '3cPDMityEM85xhq',
}

PLAYLISTS = ['spotify:playlist:5PkrnGrf4RN2UtHCad45Yu', 'spotify:playlist:5PkrnGrf4RN2UtHCad45Yu',
             'spotify:playlist:2N5MFM7E8OXrj5JEiRDRL3', 'spotify:playlist:2N5MFM7E8OXrj5JEiRDRL3',
             'spotify:playlist:37i9dQZF1DXcBWIGoYBM5M']


region = 'us-west-1'

accounts = {
    'samnickolay@gmail.com': 'Tlbsj5116',
    # 'harperyoung@vizy.io': '9RSA769PNb56!?',
    # 'genetaylor@vizy.io': '5kXcFXPLxWJL!?',
    # 'phoenixgriffiths@vizy.io': 'wGcbApcfFyKs!?',
    # 'danniwood@vizy.io': 'ZNDL6FbqVfKV!?',
    # 'alexreid@vizy.io': 'T2x98cGUC3A8!?',
    # 'chrischaney@vizy.io': 'mzhAHDkEG2He!?',
    # 'riverburton@vizy.io': 'zWQEqNEad8uh!?',
    # 'carmenmoran@vizy.io': 'x4S9ZxMR8qqj!?',
    # 'erinboone@vizy.io': 'DncBCZbMzvpF!?',
    # 'brynnratliff@vizy.io': 'vtVPXG4WVzKt!?',
    # 'skylercooke@vizy.io': 'mSM7ba9D7zuS!?',
    # 'judefletcher@vizy.io': 'RgvBZz6pWTvb!?',
    # 'drewwhite@vizy.io': 'T3PmqY6zpWqx!?',
    # 'jordanmatthews@vizy.io': 'uWnBcdteMdQH!?',
    # 'riverkaur@vizy.io': 'kFMccVuR3FjS!?',
    # 'harpernorris@vizy.io': 'XAycrx4BD2gc!?',
    # 'loganbryan@vizy.io': '9twZW4qBQMPt!?',
    # 'alexrose@vizy.io': 'wV3PWU7dy9sa!?',
    # 'rayleereed@vizy.io': '9SgUfJsAgMsZ!?',
    # 'riverallison@vizy.io': 'LYfrF8T2tqNG!?',
    # 'kaiparry@vizy.io': 'Zh2fuQLvMh5W!?',
    # 'aarenburton@vizy.io': '8ETUDLWp6nvW!?',
    # 'frankybradley@vizy.io': 'pNkMTaMgpjKu!?',
    # 'jessknight@vizy.io': 'rRLACcVUmmBc!?',
    # 'alexstone@vizy.io': 'QD4puAhj65dA!?',
    # 'geneschwartz@vizy.io': 'yLRPK2dYMhng!?',
    # 'brynncummings@vizy.io': 'pDW9bErDWKN2!?',
    # 'jessiefulton@vizy.io': 'utGHFFZbNtpS!?',
    # 'brettchang@vizy.io': 'HWvaPRnZzYfe!?',
    # 'erinknapp@vizy.io': '6uaBTV93qBN6!?',
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

vpns = ['5061', '5063', '5041', '5042', '5064', '5043', '5035', '2852', '2853', '2862', '2722', '2723', '2900', '2901', '2902', '2903', '2904', '2905', '2906', '2907', '2908', '2909', '2910', '2911', '2912', '2913', '2914', '2915', '2916', '2917', '2918', '2919', '2920', '2921', '2922', '2923', '2924', '2925', '2926', '2927', '2928', '2929', '2930', '2931', '2932', '2933', '2934', '2935', '2936', '5054', '2937', '2938', '2939', '2940', '2941', '2942', '2943', '2944', '2945', '2946', '2947', '2948', '5055', '2949', '2950', '4672', '4673', '4674', '4675', '4676', '4677', '4678', '4735', '4950', '4951', '4952', '5038', '4953', '4954', '5057', '5058', '5059', '5060', '4955', '4956', '5066', '5067', '5068', '5069', '5070', '5071', '5072', '5073', '5074', '5075', '5076', '5077', '5078', '5079', '5080', '5081', '5082', '5083', '5084', '5085', '5086', '5087', '5088', '5089', '5090', '5091', '5092', '5093', '5094', '5095', '5099', '5100', '5101', '5102', '5103', '5104', '5105', '5106', '5107', '5108', '5109', '5110', '5111', '5112', '5113', '5221', '5223', '5238', '5239', '5240', '5241', '5242', '5243', '5244', '5245', '5246', '5247', '5248', '5249', '5250', '5251', '5252', '5253', '5254', '5255', '5256', '5257', '5258', '5259', '5260', '5261', '5262', '5263', '5264', '5265', '5266', '5267', '5329', '5330', '5331', '5332', '5333', '5334', '5335', '5336', '5337', '5338', '5299', '5300', '5301', '5302', '5303', '5304', '5305', '5306', '5307', '5308', '5309', '5310', '5311', '5312', '5313', '5314', '5315', '5316', '5317', '5318', '5319', '5320', '5321', '5322', '5323', '5324', '5325', '5326', '5327', '5328', '5339', '5340', '5341', '5342', '5343', '5349', '5350', '5351', '5352', '5356', '5357', '5358', '5359', '5360', '5381', '5382', '5384', '5385', '5386', '5387', '5388', '5389', '5390', '5393', '5396', '5397', '5398', '5399', '5400', '5401', '5402', '5403', '5404', '5405', '5406', '5407', '5408', '5409', '5410', '5411', '5412', '5413', '5414', '5415', '5416', '5417', '5418', '5419', '5420', '5424', '5425', '5426', '5427', '5428', '5431', '5432', '5433', '5434', '5438', '5439', '5523', '5524', '5525', '5526', '5527', '5528', '5529', '5530', '4957', '4958', '5480', '5482', '5483', '5484', '5485', '5486', '5487', '5488', '5489', '5490', '5491', '5492', '5493', '5494', '5495', '5496', '5497', '5498', '5499', '5500', '5501', '5502', '5503', '5504', '5505', '5506', '5507', '5508', '5509', '5510', '5520', '5521', '5531', '5532', '5533', '5534', '5535', '5536', '5537', '5538', '5539', '5546', '5547', '5548', '5549', '5550', '5551', '5552', '5553', '5554', '5556', '5557', '5558', '5559', '5560', '5561', '4959', '4960', '5594', '5597', '5600', '5601', '5602', '5603', '5604', '5605', '5606', '5610', '5611', '5612', '5613', '5614', '5615', '5620', '5627', '5628', '5645', '5646', '5647', '5648', '5649', '5650', '5651', '5652', '5653', '5654', '5655', '5656', '5657', '5658', '5659', '5660', '5661', '5662', '5663', '5664', '5665', '5666', '5667', '5668', '5669', '5670', '5671', '5672', '5673', '5674', '5675', '5676', '5677', '5678', '5679', '5680', '5681', '5682', '5683', '5684', '5685', '5686', '5687', '5688', '5689', '5690', '5691', '5692', '5693', '5694', '5695', '5696', '5697', '5698', '5699', '5700', '5701', '5702', '5703', '5704', '5781', '5782', '5785', '5786', '5787', '5788', '5789', '5790', '5791', '5792', '5793', '5794', '5795', '5796', '5797', '5798', '5799', '5800', '5801', '5802', '5803', '5804', '5805', '5806', '5807', '5808', '5809', '5810', '5811', '5812', '5813', '5814', '5724', '5725', '5726', '5727', '5728', '5729', '5735', '5736', '5737', '5738', '5739', '5740', '5741', '5742', '5743', '5744', '5745', '5746', '5747', '5748', '5756', '5757', '5758', '5759', '5760', '5761', '5762', '5775', '5776', '5777', '5815', '5818', '5819', '5820', '5821', '5822', '5823', '5824', '5825', '5826', '5827', '5828', '5829', '5830', '5831', '5832', '5833', '5834', '5835', '5836', '5837', '5838', '5839', '5840', '5841', '5842', '5843', '5844', '5845', '5846', '5847', '5848', '5849', '5850', '5851', '5852', '5853', '5854', '5855', '5856', '5857', '5858', '5859', '5860', '5861', '5862', '5863', '5864', '5865', '5866', '5867', '5922', '5923', '5924', '5925', '5926', '5927', '5928', '5929', '5930', '5931', '5932', '5933', '5934', '5935', '5936', '5937', '5938', '5939', '5940', '5941', '5942', '5944', '5945', '5946', '5947', '5948', '5949', '5950', '5951', '5953', '5954', '5955', '5956', '5970', '5971', '5972', '5989', '5990', '5991', '5992', '5993', '5994', '5995', '5996', '5997', '5998', '5999', '6000', '6001', '6002', '6003', '6004', '6006', '6007', '6008', '6010', '6019', '6020', '6021', '6022', '6023', '6024', '6025', '6037', '6038', '6039', '6040', '6041', '6042', '6043', '6044', '6045', '6047', '6048', '6049', '6053', '6054', '6055', '6056', '6063', '6064', '6065', '6066', '6067', '6068', '6069', '6070', '6071', '6072', '6073', '6074', '6075', '6076', '6077', '6078', '6079', '6080', '6081', '6082', '6083', '6084', '6085', '6086', '6087', '6088', '6089', '6090', '6091', '6092', '6093', '6094', '6100', '6101', '6102', '6103', '6104', '6105', '6106', '6107', '6108', '6109', '6110', '6111', '6116', '6117', '6118', '6119', '6120', '6122', '6123', '6124', '6125', '6126', '6134', '6135', '6138', '6139', '6140', '6141', '6147', '6148', '6149', '6150', '6151', '6152', '6153', '6154', '6155', '6161', '6162', '6164', '6165', '6166', '6167', '6170', '6172', '6173', '6174', '6175', '6176', '6177', '6178', '6179', '6180', '6181', '6182', '6183', '6184', '6185', '6190', '6191', '6192', '6193', '6194', '6195', '6196', '6198', '6199', '6200', '6201', '6202', '6203', '6204', '6235', '6236', '6237', '6238', '6239', '6240', '6241', '6242', '6243', '6244', '6245', '6246', '6247', '6248', '6249', '6250', '6251', '6252', '6253', '6254', '6255', '6256', '6257', '6258', '6259', '6260', '6261', '6262', '6263', '6264', '6265', '6266', '6267', '6268', '6269', '6271', '6272', '6273', '6274', '6275', '6276', '6277', '6278', '6279', '6280', '6281', '6282', '6283', '6284', '6285', '6286', '6287', '6288', '6289', '6290', '6291', '6292', '6293', '6294', '6295', '6296', '6297', '6298', '6299', '6300', '6301', '6302', '6303', '6304', '6305', '6306', '6307', '6308', '6309', '6310', '6312', '6313', '6314', '6315', '6316', '6317', '6318', '6319', '6320', '6321', '6322', '6323', '6324', '6325', '6326', '6327', '6328', '6329', '6331', '6332', '6333', '6334', '6335', '6336', '6337', '6338', '6339', '6340', '6346', '6347', '6348', '6349', '6350', '6351', '6352', '6358', '6359', '6360', '6361', '6362', '6363', '6398', '6399', '6400', '6401', '6402', '6403', '6404', '6405', '6411', '6412', '6413', '6414', '6415', '6416', '6417', '6418', '6420', '6421', '6422', '6423', '6424', '6425', '6426', '6427', '6429', '6430', '6431', '6432', '6433', '6434', '6435', '6436', '6439', '6440', '6441', '6443', '6444', '6445', '6446', '6447', '6448', '6449', '6450', '6451', '6452', '6453', '6454', '6455', '6456', '6457', '6458', '6459', '6460', '6461', '6462', '6467', '6468', '6470', '6471', '6472', '6473', '6474', '6475', '6476', '6477', '6478', '6480', '6481', '6482', '6483', '6484', '6485', '6486', '6487', '6488', '6489', '6490', '6491', '6492', '6493', '6494', '6495', '6496', '6497', '6498', '6499', '6501', '6502', '6503', '6507', '6508', '6509', '6510', '6511', '6512', '6513', '6514', '6515', '6516', '6517', '6518', '6519', '6520', '6521', '6522', '6533', '6534', '6535', '6536', '6537', '6538', '6539', '6540', '6549', '6550', '6551', '6552', '6553', '6554', '6555', '6556', '6562', '6563', '6564', '6565', '6566', '6567', '6568', '6569', '6570', '6572', '6573', '6574', '6575', '6576', '6577', '6578', '6579', '6580', '6581', '6582', '6583', '6584', '6585', '6586', '6587', '6588', '6589', '6590', '6591', '6592',
        '6593', '6598', '6599', '6600', '6601', '6602', '6603', '6604', '6605', '6606', '6607', '6608', '6609', '6610', '6611', '6612', '6613', '6614', '6615', '6616', '6617', '6618', '6619', '6620', '6622', '6623', '6624', '6625', '6626', '6627', '6628', '6629', '6640', '6641', '6642', '6655', '6656', '6657', '6658', '6659', '6660', '6661', '6662', '6663', '6664', '6665', '6666', '6667', '6668', '6669', '6670', '6671', '6672', '6673', '6674', '6675', '6676', '6677', '6678', '6679', '6680', '6681', '6682', '6683', '6684', '6685', '6686', '6687', '6689', '6690', '6691', '6692', '6694', '6695', '6696', '6697', '6698', '6699', '6700', '6701', '6702', '6703', '6704', '6705', '6706', '6707', '6709', '6710', '6716', '6717', '6718', '6719', '6720', '6811', '6812', '6813', '6814', '6815', '6816', '6817', '6818', '6819', '6820', '6721', '6722', '6723', '6724', '6725', '6785', '6786', '6787', '6788', '6789', '6790', '6791', '6792', '6793', '6794', '6795', '6796', '6797', '6731', '6732', '6733', '6734', '6735', '6736', '6737', '6738', '6739', '6740', '6768', '6769', '6741', '6742', '6743', '6744', '6745', '6746', '6747', '6748', '6749', '6750', '6751', '6752', '6775', '6776', '6777', '6778', '6779', '6780', '6782', '6783', '6784', '6757', '6758', '6759', '6760', '6761', '6762', '6763', '6764', '6765', '6766', '6767', '6821', '6822', '6823', '6824', '6825', '6826', '6827', '6828', '6829', '6830', '6831', '6832', '6833', '6834', '6835', '6836', '6837', '6838', '6839', '6840', '6841', '6842', '6843', '6844', '6845', '6846', '6847', '6848', '6849', '6850', '6851', '6852', '6853', '6854', '6855', '6856', '6857', '6858', '6859', '6860', '6861', '6862', '6863', '6864', '6865', '6866', '6867', '6868', '6873', '6876', '6877', '6878', '6879', '6875', '6880', '6881', '6882', '6883', '6884', '6885', '6886', '6887', '6888', '6889', '6890', '6891', '6892', '6893', '6894', '6895', '6896', '6897', '6898', '6899', '6901', '6902', '6903', '6904', '6905', '6906', '6907', '6908', '6909', '6910', '6911', '6912', '6913', '6914', '6915', '6916', '6917', '6918', '6919', '6928', '6929', '6930', '6931', '6942', '6943', '6945', '6955', '6956', '6957', '6958', '6959', '6960', '6961', '6962', '6963', '6964', '6965', '6944', '6946', '6947', '6948', '6949', '6950', '6951', '6952', '6953', '6954', '6983', '6985', '6986', '6987', '6988', '6989', '6990', '6991', '6992', '6993', '6994', '6995', '6996', '6997', '6998', '6999', '8000', '8001', '8002', '8003', '8004', '8005', '8006', '8008', '8009', '8011', '8012', '8013', '8014', '8007', '4961', '4962', '8021', '8022', '8023', '8024', '8025', '8026', '8027', '8028', '8029', '8030', '8031', '8032', '8033', '8034', '8035', '8036', '8037', '8038', '8039', '8040', '8041', '8042', '8043', '8044', '8045', '8046', '8047', '8048', '8049', '8050', '8051', '8052', '8053', '8054', '8055', '8056', '8057', '8058', '8059', '8060', '8061', '8062', '8063', '8064', '8065', '8066', '8067', '8068', '8069', '8070', '8071', '8072', '8073', '8074', '8075', '8076', '8077', '8078', '8079', '8080', '8081', '8082', '8083', '8084', '8085', '8086', '8087', '8088', '8089', '8090', '8091', '8092', '8093', '8094', '8095', '8096', '8097', '8098', '8099', '8100', '8101', '8102', '8103', '8104', '8105', '8106', '8107', '8108', '8109', '8110', '8111', '8112', '8113', '8114', '8115', '8116', '8117', '8118', '8119', '8120', '8121', '8122', '8123', '8124', '8125', '8126', '8127', '8128', '8129', '8130', '8131', '8132', '8133', '8134', '8135', '8136', '8137', '8138', '8139', '8140', '8141', '8142', '8143', '8144', '8145', '8146', '8147', '8148', '8149', '8150', '8151', '8162', '8163', '8164', '8165', '8166', '8167', '8168', '8169', '8170', '8171', '8172', '8173', '8174', '8175', '8176', '8186', '8187', '8188', '8189', '8190', '8191', '8192', '8193', '8194', '8195', '8196', '8197', '8198', '8199', '8200', '8201', '8202', '8203', '8204', '8205', '8206', '8207', '8208', '8209', '8210', '8211', '8212', '8213', '8214', '8215', '8216', '8217', '8218', '8219', '8220', '8221', '8222', '8223', '8224', '8225', '8226', '8227', '8228', '8229', '8230', '8231', '8232', '8233', '8234', '8235', '8236', '8237', '8238', '8239', '8240', '8241', '8242', '8243', '8244', '8245', '8246', '8247', '8248', '8249', '8250', '8251', '8252', '8253', '8254', '8255', '8256', '8257', '8258', '8259', '8260', '8261', '8262', '8263', '8264', '8265', '8266', '8267', '8268', '8269', '8270', '8271', '8272', '8273', '8274', '8275', '8276', '8277', '8278', '8279', '8280', '8281', '4963', '4964', '8282', '8283', '8284', '8285', '8286', '8287', '8288', '8289', '8290', '8291', '8292', '8293', '8294', '8295', '8296', '8297', '8298', '8299', '8300', '8301', '8302', '8303', '8304', '8305', '8306', '8307', '8308', '8309', '8310', '8311', '8312', '8313', '8314', '8315', '8316', '8317', '8318', '8319', '8320', '8321', '8322', '8323', '8324', '8325', '8326', '8327', '8328', '8329', '8330', '8331', '8332', '8333', '8334', '8335', '8336', '8337', '8338', '8339', '8340', '8346', '8347', '8348', '8349', '8350', '8351', '8352', '8353', '8354', '8355', '8356', '8357', '8358', '8359', '8360', '8361', '8362', '8363', '8364', '8365', '8366', '8367', '8368', '8369', '8370', '8371', '8372', '8373', '8374', '8375', '8376', '8377', '8378', '8379', '8380', '8381', '8382', '8383', '8384', '8385', '8386', '8387', '8388', '8389', '8390', '8391', '4965', '4966', '8392', '8393', '8394', '8395', '8396', '8397', '8398', '8399', '8400', '8401', '8402', '8403', '8404', '8405', '8406', '8407', '8408', '8409', '8410', '8411', '8412', '8413', '8414', '8415', '8416', '8417', '8418', '8419', '8420', '8421', '8422', '8423', '8424', '8425', '8426', '8427', '8428', '8429', '8430', '8432', '8433', '8434', '8435', '8436', '8437', '8438', '8439', '8440', '8441', '8442', '8443', '8444', '8445', '8446', '8447', '8448', '8449', '8450', '8451', '8452', '8453', '8454', '8455', '8456', '8457', '8458', '8459', '8460', '8461', '8462', '8463', '8464', '8465', '8466', '8467', '8468', '8469', '8470', '8471', '8472', '8473', '8474', '8475', '8476', '8477', '8478', '8479', '8480', '8481', '8482', '8483', '8484', '8485', '8486', '8487', '8488', '8489', '8490', '8491', '8492', '8493', '8494', '8495', '8496', '8497', '8498', '8499', '8500', '8501', '8502', '8506', '8507', '8508', '8509', '8510', '8511', '8512', '8513', '8514', '8515', '8516', '8517', '8518', '8519', '8520', '8521', '8522', '8523', '8524', '8525', '8526', '8527', '8528', '8529', '8530', '8531', '8532', '8533', '8534', '8535', '8536', '8537', '8538', '8539', '8540', '8541', '8542', '8543', '8544', '8545', '8546', '8547', '8548', '8549', '8550', '8551', '8552', '8553', '8554', '8555', '8556', '8557', '8558', '8559', '8560', '8561', '8562', '8563', '8564', '8565', '8566', '8567', '8568', '8569', '8570', '8571', '8572', '8573', '8574', '8575', '8576', '8577', '8578', '8579', '8580', '8581', '8582', '8583', '8584', '8585', '8586', '8587', '8588', '8589', '8590', '8591', '8592', '8593', '8594', '8595', '8596', '8597', '8598', '8599', '8600', '8601', '8602', '8603', '8604', '8605', '8606', '8607', '8608', '8609', '8610', '8611', '8612', '8613', '8614', '8615', '8616', '8617', '8618', '8619', '8620', '8621', '8622', '8623', '8624', '8625', '8626', '8627', '8628', '8629', '8630', '8631', '8632', '8633', '8634', '8635', '8636', '8637', '8638', '8639', '8640', '8641', '8642', '8643', '8644', '8645', '8646', '8647', '8648', '8649', '8650', '8651', '8652', '8653', '8654', '8655', '8656', '8657', '8658', '8659', '8660', '8661', '8662', '8663', '8664', '8665', '8666', '8667', '8668', '8669', '8670', '8671', '8672', '8673', '8674', '8675', '8676', '8677', '8678', '8679', '8680', '8681', '8682', '8683', '8684', '8685', '8686', '8687', '8688', '8689', '8690', '8691', '8692', '8693', '8694', '8695', '8696', '8697']
random.shuffle(vpns)

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

    idx = -1
    vpn_accounts_list = [(k, v) for k, v in vpn_accounts.items()]
    spotify_accounts_list = [(k, v) for k, v in accounts.items()]

    for (email, password) in spotify_accounts_list:
        idx += 1
        tmp = int((idx - (idx % 6)) / 6)

        VPN_EMAIL = vpn_accounts_list[tmp][0]
        VPN_PASSWORD = vpn_accounts_list[tmp][1]

        PLAYLIST = random.choice(PLAYLISTS)

        print(PLAYLIST)

        vpn_name = 'us' + vpns.pop()
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
                        "Key": "vpn_name",
                        "Value": vpn_name,
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
        'body': json.dumps("Done!")
    }
