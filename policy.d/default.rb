policy :default do
  lookup :main do
    datasource :file, {
      format:     :yaml,
      docroot:    './jerakia/data',
      searchpath: ['common'],
    }
  end
end
