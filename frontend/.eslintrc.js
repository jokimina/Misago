module.exports = {
    "env": {
        "browser": true,
        "es6": true,
        "jquery": true,
        "node": true
    },
    'parser': 'babel-eslint',
    "parserOptions": {
        "ecmaFeatures": {
            "jsx": true
        },
        "ecmaVersion": 7,
        "sourceType": "module"
    },
    "rules": {
        "linebreak-style": [
            "error",
            "unix"
        ],
        "quotes": [
            "error",
            "double"
        ],
        "no-undef": "error",
        "strict": 2,       
        "semi": [
            "error",
            "never"
        ]
    },
    "globals": {
        "gettext": true,
        "ngettext": true,
        "interpolate": true,
        "misago": true,
        "hljs": true
    },
};
