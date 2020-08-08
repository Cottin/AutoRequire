

Person: _ {id: {in: [3, 4]}, ːname},
  roles: _ {ːname},
    project: _ {ːid, ːname},
      company: _ {ːname}
  entries: _ {ːdate, ːamount}


add = (a, b) -> a + b
add 1, 2

Person: 3

Person: [{id: {in: [3, 4]}}]


Person: _ {id: {in: [3, 4]}, :age}


Person: _ {id: {in: [3, 4]}, ːname},
  roles: _ {ːname},
    project: _ {ːid, ːname},
      company: _ {ːname}
  entries: _ {ːdate, ːamount}


Person: _ {name: {like: '%e%'}},
  entries: _ {:date, :amount, :text},
    task: _ {:name}
    project: _ {:name}

Person: _ {age: {gt: 50}, :ALL},
  roles: _ {:ALL},
    project: _ {:ALL},
      company: _ {:ALL}
