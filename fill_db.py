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

gta5 = Game(title = 'Grand Theft Auto V', description = 'Grand Theft Auto V is an action-adventure game played from either a first-person or third-person view.', genre_id='action', user_id=1)
db.session.add(gta5)

deadisland = Game(title = 'Dead Island', description = 'Zombie Apocolypse. Can you survive the hordes of undead?', genre_id='action', user_id=1)
db.session.add(deadisland)

bioshock = Game(title = 'BioShock', description = 'Set in 1960 in the underwater city of Rapture, with the history of the city told through audio recordings the player can collect.', genre_id='fps', user_id=1)
db.session.add(bioshock)


db.session.commit()
