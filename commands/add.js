const { SlashCommandBuilder } = require('@discordjs/builders');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('add')
        .setDescription('Adds social credit'),
    async execute(interaction) {
        await interaction.reply('+100 social credit!');
    },
};