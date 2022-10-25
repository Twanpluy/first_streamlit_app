-- Be Clear, these are just random queries, used for a snowflake badge!!!!


use role sysadmin
;

create schema mels_smoothie_challenge_db.LOCATIONS;

create or replace function mels_smoothie_challenge_db.LOCATIONS.distance_to_mc(loc_lat number(38,32), loc_lng number(38,32))
    returns float
    as
    $$
        st_distance(
        st_makepoint('-104.97300245114094','39.76471253574085')
        ,st_makepoint(loc_lat,loc_lng)
        )
    $$;
    
    
    --Tivoli Center into the variables 
set tc_lat='-105.00532059763648'; 
set tc_lng='39.74548137398218';

select distance_to_mc($tc_lat,$tc_lng);

create or replace view mels_smoothie_challenge_db.locations.COMPETITION as
select * 
from SONRA_DENVER_CO_USA_FREE.DENVER.V_OSM_DEN_AMENITY_SUSTENANCE
where 
    ((amenity in ('fast_food','cafe','restaurant','juice_bar'))
    and 
    (name ilike '%jamba%' or name ilike '%juice%'
     or name ilike '%superfruit%'))
 or 
    (cuisine like '%smoothie%' or cuisine like '%juice%');
    
    
    
    
    
    SELECT
 name
 ,cuisine
 , ST_DISTANCE(
    st_makepoint('-104.97300245114094','39.76471253574085')
    , coordinates
  ) AS distance_from_melanies
 ,*
FROM  competition
ORDER by distance_from_melanies;



CREATE OR REPLACE FUNCTION distance_to_mc(lat_and_lng GEOGRAPHY)
  RETURNS FLOAT
  AS
  $$
   st_distance(
        st_makepoint('-104.97300245114094','39.76471253574085')
        ,lat_and_lng
        )
  $$
  ;
  
  
SELECT
 name
 ,cuisine
 ,distance_to_mc(coordinates) AS distance_from_melanies
 ,*
FROM  competition
ORDER by distance_from_melanies;


create or replace view mels_smoothie_challenge_db.locations.DENVER_BIKE_SHOPS
as
select * , distance_to_mc(coordinates) AS DISTANCE_TO_MELANIES

from sonra_denver_co_usa_free.denver.v_osm_den_shop_outdoors_and_sport_vehicles
where shop = 'bicycle' and 
DISTANCE_TO_MELANIES =  2,490 
