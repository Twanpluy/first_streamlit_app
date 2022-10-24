use role sysadmin;
create database MELS_SMOOTHIE_CHALLENGE_DB;
drop schema MELS_SMOOTHIE_CHALLENGE_DB.public;
create schema MELS_SMOOTHIE_CHALLENGE_DB.TRAILS;

create stage <stage_name>
    url = '<url>'
    credentials = (aws_secret_key = '<key>' aws_key_id = '<id>');
    
create or replace stage mels_smoothie_challenge_db.trails.trails_geojson
 url = 's3://uni-lab-files-more/dlkw/trails/trails_geojson';
 
 list @mels_smoothie_challenge_db.trails.trails_geojson;    

    
create or replace stage mels_smoothie_challenge_db.trails.trails_parquet
 url = 's3://uni-lab-files-more/dlkw/trails/trails_parquet';
 
 list @mels_smoothie_challenge_db.trails.trails_parquet;

 create or replace file format mels_smoothie_challenge_db.trails.FF_JSON
type = 'JSON'

create or replace file format mels_smoothie_challenge_db.trails.FF_PARQUET
type = 'PARQUET'

use role sysadmin;

create or replace view mels_smoothie_challenge_db.trails.CHERRY_CREEK_TRAIL as
select $1:sequence_1 as point_id,
       $1:trail_name::varchar as TRAIL_NAME,
       $1:latitude::number(11,8) as lng,
       $1:longitude::number(11,8) as lat,
       $1:sequence_2 as sequence_2,
       $1:elevation as elevation
from @trails_parquet
(file_format => ff_parquet)
order by point_id

select top 100
cct.lng||' '||lat as coord_pair,
'POINT('||coord_pair||')' as trail_point
from mels_smoothie_challenge_db.trails.cherry_creek_trail  cct;

--To add a column, we have to replace the entire view
--changes to the original are shown in red
create or replace view cherry_creek_trail as
select 
 $1:sequence_1 as point_id,
 $1:trail_name::varchar as trail_name,
 $1:latitude::number(11,8) as lng,
 $1:longitude::number(11,8) as lat,
 lng||' '||lat as coord_pair
from @trails_parquet
(file_format => ff_parquet)
order by point_id;

select 
'LINESTRING('||
listagg(coord_pair, ',') 
within group (order by point_id)
||')' as my_linestring
from cherry_creek_trail
where point_id <= 100
group by trail_name;

use role sysadmin;


create or replace view mels_smoothie_challenge_db.trails.DENVER_AREA_TRAILS as
select
 $1:features[0]:properties:Name::string as feature_name
,$1:features[0]:geometry:coordinates::string as feature_coordinates
,$1:features[0]:geometry::string as geometry
,st_length(TO_GEOGRAPHY(geometry)) as trail_length
,$1:features[0]:properties::string as feature_properties
,$1:crs:properties:name::string as specs
,$1 as whole_object
from @trails_geojson (file_format => ff_json);


select * from mels_smoothie_challenge_db.trails.denver_area_trails;


--Remember this code? 
select 
'LINESTRING('||
listagg(coord_pair, ',') 
within group (order by point_id)
||')' as my_linestring
,st_length(TO_GEOGRAPHY(my_linestring)) as length_of_trail 
from cherry_creek_trail
group by trail_name;

--Create a view that will have similar columns to DENVER_AREA_TRAILS 
select feature_name, to_geography(geometry) as my_linestring, trail_length
from DENVER_AREA_TRAILS
union all
select feature_name, to_geography(geometry) as my_linestring, trail_length
from DENVER_AREA_TRAILS_2;



create view mels_smoothie_challenge_db.trails.TRAILS_AND_BOUNDARIES as
--Add more GeoSpatial Calculations to get more GeoSpecial Information! 
select feature_name
, to_geography(geometry) as my_linestring
, st_xmin(my_linestring) as min_eastwest
, st_xmax(my_linestring) as max_eastwest
, st_ymin(my_linestring) as min_northsouth
, st_ymax(my_linestring) as max_northsouth
, trail_length
from DENVER_AREA_TRAILS
union all
select feature_name
, to_geography(geometry) as my_linestring
, st_xmin(my_linestring) as min_eastwest
, st_xmax(my_linestring) as max_eastwest
, st_ymin(my_linestring) as min_northsouth
, st_ymax(my_linestring) as max_northsouth
, trail_length
from DENVER_AREA_TRAILS_2;

select * from TRAILS_AND_BOUNDARIES;
