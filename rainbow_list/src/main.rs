
use std::cmp::Ordering;
// use std::ops::Index;
use std::rc::Rc;

////

// list indices (bounds list length)
type Ind = i32;

// largest power of 2 dividing i
fn k_(i: Ind) -> Ind { i & -i }

// hop deltas
fn dr(i: Ind) -> Ind { k_(i) >> 1 }
fn dg(i: Ind) -> Ind { k_(i) }
fn db(i: Ind) -> Ind { k_(i) << 1 }

// hop targets
fn r_(i: Ind) -> Ind { i-dr(i) }
fn g_(i: Ind) -> Ind { i-dg(i) }
fn b_(i: Ind) -> Ind { i-db(i) }

////

type Link<T> = Option<Rc<Node<T>>>;

#[derive(Debug)]
pub struct RList<T> { head: Link<T> }

impl<T> Clone for RList<T> {
    fn clone(&self) -> Self {
        Self { head: self.head.clone() }
    }
}

#[derive(Debug)]
struct Node<T> {
    v: T,       // value
    i: Ind,     // index
    n: Link<T>, // next
    r: Link<T>, // red
    g: Link<T>, // green
    b: Link<T>, // blue
}

fn i_<T>(link: &Link<T>) -> Ind { 
    match link { Some(hd) => hd.i, None => 0 } // link.as_ref().map(|x| x.i).unwrap_or(0)
}

////

impl<T> RList<T> {
    pub const NULL: Self = Self { head: None };

    pub fn new() -> Self {
        Self { head: None }
    }

    pub fn append(&self, v: T) -> Self {
        // i = self.i+1
        // n = self
        // k = i & -i
        // # red
        // if k == 1:          r = None
        // elif k == 2:        r = n
        // else:               r = n.b
        // # green
        // if k == 1:          g = n
        // else:               g = r.g
        // # blue
        // if i & (k<<1):
        //     if i & (k<<2):  b = g.b
        //     else:           b = g
        // elif i > (k<<1):
        //     if k == 1:      b = n.n
        //     else:           b = r.b.g
        // else:               b = None
        // return Node(v, i, n, r, g, b)

        let i = i_(&self.head)+1;
        let n = self.head.clone();
        let k = k_(i);
        // red
        let r = match k {
            1 => None,
            2 => n.clone(),
            _ => n.as_ref().and_then(|x| x.b.clone()),
        };
        // green
        let g = if k == 1 { n.clone() } else { r.as_ref().and_then(|x| x.g.clone()) };
        // blue
        let b = if (i & k<<1) != 0 {
            if (i & k<<2) != 0 { g.as_ref().and_then(|x| x.b.clone()) } else { g.clone() }
        } else if i > k<<1 {
            if k == 1 { n.as_ref().and_then(|x| x.n.clone()) } else { r.as_ref().and_then(|x| x.b.as_ref()).and_then(|x| x.g.clone()) }
        } else { None };

        Self { head: Some(Rc::new(Node { v, i, n, b, g, r, }))}
    }

    pub fn tail(&self) -> Self {
        Self { head: self.head.as_ref().and_then(|node| node.n.clone()) }
    }

    pub fn head(&self) -> Option<&T> {
        self.head.as_ref().map(|node| &node.v)
    }

    pub fn iter(&self) -> Iter<'_, T> {
        Iter { next: self.head.as_ref().map(|node| &**node) }
    }

    fn seek_link(&self, ind: Ind) -> Link<T> {
        if ind <= 0 { return None }

        match i_(&self.head).cmp(&ind) {
            Ordering::Less => None,
            Ordering::Equal => self.head.clone(),
            Ordering::Greater => { 
                let mut head: Link<T> = self.head.clone();
                let mut i: Ind = i_(&head);
                while i > ind {
                    println!("i: {:?}", i);
                    if      g_(i) >= ind && g_(g_(i)) >= g_(ind) { head = head.and_then(|x| x.g.clone()) }
                    else if b_(i) >= ind && g_(b_(i)) >= g_(ind) { head = head.and_then(|x| x.b.clone()) }
                    else if r_(i) >= ind && g_(r_(i)) >= g_(ind) { head = head.and_then(|x| x.r.clone()) } //.or_else(|| x.n.clone())) }
                    else { head = head.and_then(|x| x.g.clone()) }
                    i = i_(&head)
                }
                println!("i: {:?}", i);
                head
            },
        }
    }

    pub fn seek(&self, ind: Ind) -> Self { 
        Self { head: self.seek_link(ind) } 
    }

    pub fn slice(&self, i: Ind) -> Self {
        let ind = i_(&self.head) - i;
        Self { head: self.seek_link(ind) } 
    }

    // pub fn get(&self, i: Ind) -> Option<&T> {
    //     // let ind = i_(&self.head) - i;
    //     // let sought = self.seek(ind);
    //     // sought.head()
    //     // sought.head.as_ref().map(|x| x.v)
    //     let sliced = self.slice(i);
    //     sliced.head()
    // }
}


// impl<T> Index<Ind> for RList<T> {
//     type Output = Option<&T>;
//     // FIXME: self must outlive the output
//     fn index(&self, j: Ind) -> &Self::Output { 
//         let ind = i_(&self.head) - j;
//         let sought = self.seek(ind);
//         &sought.head()
//     }
// }

impl<T> Drop for RList<T> {
    fn drop(&mut self) {
        let mut head = self.head.take();
        while let Some(node) = head {
            if let Ok(mut node) = Rc::try_unwrap(node) {
                head = node.n.take();
            } else {
                break;
            }
        }
    }
}

pub struct Iter<'a, T> {
    next: Option<&'a Node<T>>,
}

impl<'a, T> Iterator for Iter<'a, T> {
    type Item = &'a T;

    fn next(&mut self) -> Option<Self::Item> {
        self.next.map(|node| {
            self.next = node.n.as_ref().map(|node| &**node);
            &node.v
        })
    }
}

////

fn main() {
    let mut list = RList::new();
    for _ in 0..63 {
        list = list.append("hi")
    }
    // list.seek(3);
    list.slice(60);
}
