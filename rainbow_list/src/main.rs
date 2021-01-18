
use std::rc::Rc;

////

// hop deltas
fn dr(i: i64) -> i64 { dg(i) >> 1 }
fn dg(i: i64) -> i64 { i & -i }
fn db(i: i64) -> i64 { dg(i) << 1 }

// hop targets
fn r(i: i64) -> i64 { i-dr(i) }
fn g(i: i64) -> i64 { i-dg(i) }
fn b(i: i64) -> i64 { i-db(i) }

////

type Link<T> = Option<Rc<Node<T>>>;

#[derive(Debug)]
pub struct List<T> { head: Link<T> }

#[derive(Debug)]
struct Node<T> {
    v: T,       // value
    i: i64,     // index
    n: Link<T>, // next
    // r: Link<T>, // red
    // g: Link<T>, // green
    // b: Link<T>, // blue
}

fn i<T>(link: &Link<T>) -> i64 { 
    match link { Some(hd) => hd.i, None => 0 } 
}

impl<T> List<T> {
    pub fn new() -> Self {
        List { head: None }
    }

    pub fn append(&self, v: T) -> List<T> {
        List { head: Some(Rc::new(Node {
            v: v,
            i: i(&self.head)+1,
            n: self.head.clone(),
            // r: self.head.clone(),   // TODO:
            // g: self.head.clone(),   // TODO:
            // b: self.head.clone(),   // TODO:
        }))}
    }

    pub fn tail(&self) -> List<T> {
        List { head: self.head.as_ref().and_then(|node| node.n.clone()) }
    }

    pub fn head(&self) -> Option<&T> {
        self.head.as_ref().map(|node| &node.v)
    }

    pub fn iter(&self) -> Iter<'_, T> {
        Iter { next: self.head.as_ref().map(|node| &**node) }
    }
}

impl<T> Drop for List<T> {
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
    println!("r(12): {}", r(12));
    println!("g(12): {}", g(12));
    println!("b(12): {}", b(12));

    let list = List::new().append(1).append(2).append(3);
    println!("list: {:?}", list);
}


