// keyboard keys
let UP =     'up';
let DOWN =   'dn';
let LEFT =   'lf';
let RIGHT =  'rt';
let SPACE =  ' ';

// keypad keys
let KW = 'w';
let KS = 's';
let KA = 'a';
let KD = 'd';
let NZERO = '0';

let START = 'start_game';
let CLOSE = 'end_game';
let KEYPRESS = 'key_press';
let ESCAPE = null;
let RETURN = null;


// both bottom
const initPingParam = {
    'gameType': 'Ping',
    'sizeInfo': {
        'width': 2048, 'height': 1024,
        'wRatio': 0.00048828125, 'hRatio': 0.0009765625,
        'rSize': 160, 'bSize': 20
    },
    'racketCount': 2,
    'teamCount': 2,
    'orientations': ['x', 'x'],
    'update': {
        'racketPos': [682, 1004, 1365, 1004 ],
        'ballPos': [1024, 682],
        'score' : [0, 0],
    }
    // 'racketInitPos': [682, 1004, 'x', 1365, 1004, 'x'],
    // 'ballInitPos': [1024, 682],
};

// in front of each other
const initPongParam = {
     'gameType': 'Pong', 
     'sizeInfo': {
        'width': 2048, 'height': 1024, 
        'wRatio': 0.00048828125, 'hRatio': 0.0009765625, 
        'rSize': 160, 'bSize': 20
    }, 
    'racketCount': 2, 
    'teamCount': 2,
    'orientations': ['x', 'x'],
    'update': {
        'racketPos': [20, 512, 2028, 512],
        'ballPos': [512, 512],
        'score' : [0, 0],
    }
    // 'racketInitPos': [20, 512, 'y', 2028, 512, 'y'], 
    // 'ballInitPos': [512, 512], 
};

// 4 players
const initPingestParam = {
    'gameType': 'Pingest', 
    'sizeInfo': {
        'width': 1536, 'height': 1024, 
        'wRatio': 0.0006510416666666666, 'hRatio': 0.0009765625, 
        'rSize': 160, 'bSize': 20},
    'racketCount': 4, 
    'teamCount': 4,
    'orientations': ['x', 'x', 'x', 'x'],
    'update': {
        'racketPos': [438, 20, 1097, 20, 438, 1004, 1097, 1004],
        'ballPos': [512, 512],
        'score' : [0, 0],
    }
    // 'racketInitPos': [438, 20, 'x', 1097, 20, 'x', 438, 1004, 'x', 1097, 1004, 'x'], 
    // 'ballInitPos': [1152, 768],
}