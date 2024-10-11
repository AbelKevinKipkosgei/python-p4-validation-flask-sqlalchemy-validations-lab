from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('name', 'phone_number')
    def validates_authors_fields(self, key, value):
        if key == 'name':
            author_name = value

            if not author_name or author_name.strip() == '':
                raise ValueError("Author name is required!")
            
            existing_name = Author.query.filter_by(name = author_name).first()
            if existing_name:
                raise ValueError("Author name already exists.")
            
            return author_name
        
        if key == 'phone_number':
            author_number = value

            compact_number = str(author_number).replace(' ', '')

            if not compact_number.isdigit():
                raise ValueError("Phone number can only contain digits.")

            if len(compact_number) != 10:
                raise ValueError("Phone number must be exactly 10 digits.")
            
            return compact_number
    

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('title', 'content', 'category', 'summary')
    def validates_posts_fields(self, key, value):
        if key == 'content':
            post_content = value

            formatted_post_content = str(post_content).replace(' ','')
            
            if len(formatted_post_content) < 250:
                raise ValueError("Content must be at least 250 characters long!")
            
            return post_content
        
        if key == 'title':
            post_title = value

            click_bait = ["Won't Believe", "Secret", "Top", "Guess"]

            if not post_title and post_title.strip() == '':
                raise ValueError("Each post must have a title!")
            
            if not any(term in post_title for term in click_bait):
                raise ValueError(f"Title must have at least one of the following terms: {', '.join(click_bait)}")
            
            return post_title
        
        if key == 'summary':
            post_summary = value

            formatted_post_summary = str(post_summary).replace(' ','')

            if len(formatted_post_summary) > 250:
                raise ValueError("Summary cannot exceed 250 characters!")
            
            return post_summary
        
        if key == 'category':
            post_category = value

            valid_categories = ['Fiction', 'Non-Fiction']

            if post_category not in valid_categories:
                raise ValueError("Category can only be Fiction or Non-Fiction")
            
            return post_category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
