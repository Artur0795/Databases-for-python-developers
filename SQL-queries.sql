CREATE TABLE IF NOT EXISTS genre(
	id SERIAL primary key,
	genre_name VARCHAR(40) not null
);
CREATE TABLE IF NOT EXISTS artist(
	id SERIAL primary key,
	nickname VARCHAR(40) not null
);
CREATE TABLE IF NOT EXISTS item_supplier(
	id SERIAL primary key,
	artist_id INTEGER not null references artist(id),
	genre_id INTEGER not null references genre(id)
);
CREATE TABLE IF NOT EXISTS album(
	id SERIAL primary key,
	album_name VARCHAR(40) not null,
	release_year DATE not null
);
CREATE TABLE IF NOT EXISTS item_supplier2(
	id SERIAL primary key,
	artist_id INTEGER not null references artist(id),
	album_id INTEGER not null references album(id)
);
CREATE TABLE IF NOT EXISTS song(
	id SERIAL primary key,
	song_name VARCHAR(40) not null,
	duration INTEGER not null,
	album_id INTEGER not null references album(id)
);
CREATE TABLE IF NOT EXISTS collection(
	id SERIAL primary key,
	collection_name VARCHAR(40) not null,
	release_year DATE not null
);
CREATE TABLE IF NOT EXISTS trackscollections(
	id SERIAL primary key,
	song_id INTEGER not null references song(id),
	collection_id INTEGER not null references collection(id)
);