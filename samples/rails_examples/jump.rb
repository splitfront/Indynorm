MARKDOWN = Redcarpet::Markdown.new(CommentRenderer.new(filter_html: true,
                                                       no_images: true,
                                                       no_styles: true,
                                                       safe_links_only: true), extensions = {autolink: true, strikethrough: true})