from app import db
from app.models import User, Game, Genre

db.create_all()

action = Genre('Action')
action.description = 'Fast paced and invigorating'
db.session.add(action)

adventure = Genre('Adventure')
adventure.description = 'Find your way, or die.'
db.session.add(adventure)

arcade = Genre('Arcade')
arcade.description = 'Oldschool games for casual gamers'
db.session.add(arcade)

fighting = Genre('Fighting')
fighting.description = 'Hand-to-hand combat.'
db.session.add(fighting)

fps = Genre('FPS')
fps.description = 'First-person shooter'
db.session.add(fps)

puzzle = Genre('Puzzle')
puzzle.description = 'Mind-boggling games for the braniacs'
db.session.add(puzzle)

sim = Genre('Simulation')
sim.description = 'From flight to city, this is real life.'
db.session.add(sim)

sports = Genre('Sports')
sports.description = 'Based off of real life sports!'
db.session.add(sports)

strategy = Genre('Strategy')
strategy.description = 'Plan your next move carefully.'
db.session.add(strategy)

pat = User('Pat', 'prallen90@gmail.com')
db.session.add(pat)

gta5 = Game(title='Grand Theft Auto V',
            description='Grand Theft Auto V is an action-adventure game played from either a first-person or third-person view.', genre_id='action', user_id=1)
db.session.add(gta5)

deadisland = Game(title='Dead Island',
                  description='Zombie Apocolypse. Can you survive the hordes of undead?', genre_id='action', user_id=1)
db.session.add(deadisland)

bioshock = Game(title='BioShock',
                description='Set in 1960 in the underwater city of Rapture, with the history of the city told through audio recordings the player can collect.', genre_id='fps', user_id=1)
db.session.add(bioshock)

GoT = Game(title='Game of Thrones: Episode One',
           description='The series is based on the world, characters and events seen in HBO\'s television show, which in turn is based on George R. R. Martin\'s books (A Song of Ice and Fire). The events in the game series begin towards the end of Season 3 of the television show and end just before the beginning of Season 5. You\'ll traverse familiar locations such as King\'s Landing and The Wall, as well as unfamiliar locations such as Ironrath, the home of House Forrester.',
           genre_id='action', user_id=1)
db.session.add(GoT)

stf = Game(title='Super Time Force',
           description='Super Time Force is a side-scrolling action and shooter video game by Capybara Games, released for the Xbox 360\'s Live Arcade service and Xbox One. It was released on May 14, 2014.',
           genre_id='action', user_id=1)
db.session.add(stf)

simcity = Game(title='SimCity',
               description='SimCity is an open-ended city-building computer and console video game series originally designed by developer Will Wright. It is published by Maxis.',
               genre_id='simulation', user_id=1)
db.session.add(simcity)

minecraft = Game(title='Minecraft',
                 description='Minecraft is a sandbox independent video game originally created by Swedish programmer Markus \'Notch\' Persson and later developed and published by the Swedish company Mojang.',
                 genre_id='adventure', user_id=1)

walkingdead = Game(title='The Walking Dead: The Game',
                         description='Cartoon adventure game based of the television series "The Walking Dead"',
                         genre_id='adventure', user_id=1)
db.session.add(walkingdead)

tetris = Game(title='Tetris',
              description='Tetris is a Soviet tile-matching puzzle video game originally designed and programmed by Alexey Pajitnov. It was released on June 6, 1984, while he was working for the Dorodnicyn Computing Centre of the Academy of Science of the USSR in Moscow.',
              genre_id='puzzle', user_id=1)
db.session.add(tetris)

tf2 = Game(title='Team Fortress 2',
           description='Team Fortress 2 is a team-based first-person shooter multiplayer video game developed by Valve Corporation. It is the sequel to the 1996 mod Team Fortress for Quake and its 1999 remake.',
           genre_id='fps', user_id=1)
db.session.add(tf2)

csgo = Game(title='Counter-Strike: Global Offensive',
            description='Counter-Strike: Global Offensive is an online tactical first-person shooter developed by Valve Corporation and Hidden Path Entertainment, who also maintained Counter-Strike: Source after its release.',
            genre_id='fps', user_id=1)
db.session.add(csgo)

madden15 = Game(title='Madden NFL 15',
            description='Madden NFL 15 is an American football sports video game based on the National Football League and published by EA Sports.',
            genre_id='sports', user_id=1)
db.session.add(madden15)

print("Games: %s" % db.session.query(Game).count())

db.session.commit()