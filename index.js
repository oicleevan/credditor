const { Client, Intents } = require('discord.js')
const sys = require('process');

const prefix = require('./config.json')

var token

if(sys.argv[2] != null) {
	token = sys.argv[2];
} else {
	console.log("Please include an oauth password.");
	sys.exit();
}

const client = new Client({intents: [Intents.FLAGS.GUILDS] })

client.once('ready', () => {
    console.log('The bot is now enabled.');
})

client.login(token)