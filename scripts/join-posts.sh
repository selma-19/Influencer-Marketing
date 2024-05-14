#execute this script in mongosh console
#change the collection name according to the name of your collection
db.newPosts.aggregate([
  {
    $project: {
      id: 1,
      owner: 1,
      caption: {
        $arrayElemAt: [
          "$edge_media_to_caption.edges.node.text",
          0
        ]
      }
    }
  },
  {
    $group: {
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
    $set: {
      posts: {
        $reduce: {
          input: "$posts",
          initialValue: "",
          in: {
            $concat: ["$$value", " ", "$$this"]
          }
        }
      }
    }
  }
])