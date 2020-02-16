# == Schema Information
#
# Table name: backoffice_comments
#
#  id          :bigint(8)        not null, primary key
#  post_id     :integer          not null
#  author_id   :integer          not null
#  body        :string(4096)     not null
#  body_source :string(2048)     not null
#  created_at  :datetime         not null
#  updated_at  :datetime         not null
#

class BackofficeComment < ApplicationRecord

  # @!attribute post_id
  #   ID of the Post the comment belongs to, not nil. See also belongs_to :post
  #   @return [Integer]

  # @!attribute author_id
  #   ID of the User that left this comment, not nil. See also belongs_to :author
  #   @return [Integer]

  # @!attribute body
  #   Body of the comment in HTML form, generated from the markdown source, 4096 symbols max, not nil.
  #   Should be displayed via html_safe, should not be edited.
  #   @return [String]

  # @!attribute body_source
  #   Source of the comment's body in Markdown form, rendered to body attribute on save, 2048 symbols max, not nil.
  #   Should be edited, should not be displayed, unless in edit form.
  #   @return [String]

  belongs_to :author, class_name: 'User', touch: true
  belongs_to :post
  validates :body, presence: true, length: { maximum: 4096 }
  validates :body_source, presence: true, length: { maximum: 2048 }

  MARKDOWN = Redcarpet::Markdown.new(CommentRenderer.new(filter_html: true,
                                                         no_images: true,
                                                         no_styles: true,
                                                         safe_links_only: true), extensions = {autolink: true, strikethrough: true})

  before_validation do
    render
  end

  def render
    self.body = ( self.body_source.nil? ? ' ' : MARKDOWN.render(self.body_source))
  end
end
