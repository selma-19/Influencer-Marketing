#execute this script in mongosh console
#change the collection name according to the name of your collection
db.newPosts.aggregate([
  {
    $unset:
      /**
       * Provide the field name to exclude.
       * To exclude multiple fields, pass the field names in an array.
       */
      "shortcode"
  },
  {
    $group:
      /**
       * _id: The id of the group.
       * fieldN: The first field name.
       */
      {
        _id: "$owner.id",
        post_ids: {
          $push: "$$ROOT.id"
        },
        posts: {
          $push: "$$ROOT.caption"
        }
      }
  },
  {
    $set:
      /**
       * specifications: The fields to
       *   include or exclude.
       */
      {
        posts: {
          $reduce: {
            input: "$posts",
            initialValue: "",
            in: {
              $concat: ["$$value", "$$this"]
            }
          }
        }
      }
  },
  {
    $out:
      /**
       * Provide the name of the output database and collection.
       */
      {
        db: "InfluencersMarketing",
        coll: "joinedPosts"
        /*
    timeseries: {
    timeField: 'field',
    bucketMaxSpanSeconds: 'number',
    granularity: 'granularity'
    }
    */
      }
  }
])